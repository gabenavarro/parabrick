"""
VCF to FASTA Pipeline
=====================
Applies variants from a VCF file to a reference FASTA file and generates
a consensus sequence with validation steps.

Uses bcftools consensus (standard tool) for applying variants.

Examples:
  %(prog)s -f reference.fasta -v variants.vcf -o output.fasta
  %(prog)s -f ref.fa -v vars.vcf.gz -o consensus.fa --log pipeline.log

Requirements:
  - bcftools
  - samtools
  - bgzip/tabix (from htslib)
  
  Install with: conda install -c bioconda bcftools samtools htslib

"""

import subprocess
import hashlib
from pathlib import Path
from datetime import datetime

class VCFtoFASTAPipeline:
    """Pipeline for applying VCF variants to reference FASTA."""
    
    def __init__(self, fasta_path, vcf_path, output_path, log_file=None):
        self.fasta_path = Path(fasta_path)
        self.vcf_path = Path(vcf_path)
        self.output_path = Path(output_path)
        self.log_file = log_file or f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Validate inputs
        if not self.fasta_path.exists():
            raise FileNotFoundError(f"FASTA file not found: {fasta_path}")
        if not self.vcf_path.exists():
            raise FileNotFoundError(f"VCF file not found: {vcf_path}")
    
    def log(self, message):
        """Log message to file and stdout."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(self.log_file, 'a') as f:
            f.write(log_msg + '\n')
    
    def run_command(self, cmd, description):
        """Run a shell command with error handling."""
        self.log(f"Running: {description}")
        self.log(f"Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.stdout:
                self.log(f"Output: {result.stdout}")
            return result
        except subprocess.CalledProcessError as e:
            self.log(f"ERROR: {description} failed")
            self.log(f"Error message: {e.stderr}")
            raise
    
    def check_dependencies(self):
        """Check if required tools are installed."""
        self.log("Checking dependencies...")
        required_tools = ['bcftools', 'samtools', 'bgzip', 'tabix']
        
        missing_tools = []
        for tool in required_tools:
            try:
                subprocess.run([tool, '--version'], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE,
                             check=True)
                self.log(f"✓ {tool} found")
            except (subprocess.CalledProcessError, FileNotFoundError):
                missing_tools.append(tool)
                self.log(f"✗ {tool} NOT found")
        
        if missing_tools:
            raise RuntimeError(
                f"Missing required tools: {', '.join(missing_tools)}\n"
                f"Install with: conda install -c bioconda bcftools samtools htslib"
            )
    
    def index_fasta(self):
        """Index FASTA file if not already indexed."""
        fai_path = Path(str(self.fasta_path) + '.fai')
        
        if fai_path.exists():
            self.log(f"FASTA index already exists: {fai_path}")
        else:
            self.log("Indexing FASTA file...")
            self.run_command(
                ['samtools', 'faidx', str(self.fasta_path)],
                "FASTA indexing"
            )
    
    def compress_and_index_vcf(self):
        """Compress and index VCF file if needed."""
        # Check if VCF is already compressed
        if str(self.vcf_path).endswith('.gz'):
            compressed_vcf = self.vcf_path
            self.log(f"VCF is already compressed: {compressed_vcf}")
        else:
            # Compress VCF
            compressed_vcf = Path(str(self.vcf_path) + '.gz')
            if compressed_vcf.exists():
                self.log(f"Compressed VCF already exists: {compressed_vcf}")
            else:
                self.log("Compressing VCF file...")
                self.log(f"Command: bgzip -c {self.vcf_path} > {compressed_vcf}")
                
                # CRITICAL FIX: bgzip outputs binary data, handle it properly
                try:
                    with open(compressed_vcf, 'wb') as f:
                        result = subprocess.run(
                            ['bgzip', '-c', str(self.vcf_path)],
                            stdout=f,
                            stderr=subprocess.PIPE,
                            check=True
                        )
                        if result.stderr:
                            stderr_msg = result.stderr.decode('utf-8', errors='replace')
                            if stderr_msg.strip():
                                self.log(f"bgzip stderr: {stderr_msg}")
                    
                    self.log(f"VCF compressed successfully")
                    
                except subprocess.CalledProcessError as e:
                    self.log(f"ERROR: VCF compression failed")
                    stderr_msg = e.stderr.decode('utf-8', errors='replace') if e.stderr else 'Unknown error'
                    self.log(f"Error message: {stderr_msg}")
                    raise
        
        # Index VCF
        tbi_path = Path(str(compressed_vcf) + '.tbi')
        if tbi_path.exists():
            self.log(f"VCF index already exists: {tbi_path}")
        else:
            self.log("Indexing VCF file...")
            self.run_command(
                ['tabix', '-p', 'vcf', str(compressed_vcf)],
                "VCF indexing"
            )
        
        return compressed_vcf
    
    def get_file_stats(self, filepath):
        """Get basic statistics about a FASTA file."""
        stats = {
            'num_sequences': 0,
            'total_length': 0,
            'md5': None
        }
        
        md5_hash = hashlib.md5()
        
        with open(filepath, 'r') as f:
            current_seq = []
            for line in f:
                md5_hash.update(line.encode())
                line = line.strip()
                if line.startswith('>'):
                    if current_seq:
                        stats['total_length'] += len(''.join(current_seq))
                        current_seq = []
                    stats['num_sequences'] += 1
                else:
                    current_seq.append(line)
            
            # Don't forget the last sequence
            if current_seq:
                stats['total_length'] += len(''.join(current_seq))
        
        stats['md5'] = md5_hash.hexdigest()
        return stats
    
    def count_vcf_variants(self, vcf_path):
        """Count number of variants in VCF file."""
        result = subprocess.run(
            ['bcftools', 'view', '-H', str(vcf_path)],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    
    def apply_variants(self, compressed_vcf):
        """Apply variants to reference using bcftools consensus."""
        self.log("Applying variants to reference...")
        
        with open(self.output_path, 'w') as outfile:
            result = subprocess.run(
                ['bcftools', 'consensus', '-f', str(self.fasta_path), str(compressed_vcf)],
                stdout=outfile,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            
            if result.stderr:
                self.log(f"bcftools stderr: {result.stderr}")
    
    def validate_output(self):
        """Validate the output FASTA file."""
        self.log("\n" + "="*60)
        self.log("VALIDATION REPORT")
        self.log("="*60)
        
        # Get statistics
        self.log("\nInput FASTA statistics:")
        input_stats = self.get_file_stats(self.fasta_path)
        self.log(f"  Number of sequences: {input_stats['num_sequences']}")
        self.log(f"  Total length: {input_stats['total_length']:,} bp")
        self.log(f"  MD5 checksum: {input_stats['md5']}")
        
        self.log("\nOutput FASTA statistics:")
        output_stats = self.get_file_stats(self.output_path)
        self.log(f"  Number of sequences: {output_stats['num_sequences']}")
        self.log(f"  Total length: {output_stats['total_length']:,} bp")
        self.log(f"  MD5 checksum: {output_stats['md5']}")
        
        # Validation checks
        self.log("\nValidation checks:")
        checks_passed = True
        
        # Check 1: Number of sequences should match
        if input_stats['num_sequences'] == output_stats['num_sequences']:
            self.log(f"  ✓ Number of sequences matches")
        else:
            self.log(f"  ✗ WARNING: Number of sequences differs!")
            checks_passed = False
        
        # Check 2: MD5 should differ (changes were made)
        if input_stats['md5'] != output_stats['md5']:
            self.log(f"  ✓ Output differs from input (variants applied)")
        else:
            self.log(f"  ✗ WARNING: Output identical to input (no changes made?)")
            checks_passed = False
        
        # Check 3: Output file should exist and have content
        if self.output_path.exists() and self.output_path.stat().st_size > 0:
            self.log(f"  ✓ Output file exists and has content")
        else:
            self.log(f"  ✗ ERROR: Output file is missing or empty!")
            checks_passed = False
        
        # Check 4: Length difference
        length_diff = output_stats['total_length'] - input_stats['total_length']
        self.log(f"\n  Length change: {length_diff:+,} bp")
        
        self.log("\n" + "="*60)
        if checks_passed:
            self.log("✓ VALIDATION PASSED")
        else:
            self.log("✗ VALIDATION FAILED - Review warnings above")
        self.log("="*60 + "\n")
        
        return checks_passed
    
    def run(self):
        """Run the complete pipeline."""
        try:
            self.log("="*60)
            self.log("VCF to FASTA Pipeline")
            self.log("="*60)
            self.log(f"Input FASTA: {self.fasta_path}")
            self.log(f"Input VCF: {self.vcf_path}")
            self.log(f"Output FASTA: {self.output_path}")
            self.log(f"Log file: {self.log_file}")
            self.log("="*60 + "\n")
            
            # Step 1: Check dependencies
            self.check_dependencies()
            
            # Step 2: Index FASTA
            self.index_fasta()
            
            # Step 3: Compress and index VCF
            compressed_vcf = self.compress_and_index_vcf()
            
            # Step 4: Count variants
            num_variants = self.count_vcf_variants(compressed_vcf)
            self.log(f"\nNumber of variants in VCF: {num_variants}")
            
            # Step 5: Apply variants
            self.apply_variants(compressed_vcf)
            
            # Step 6: Validate
            validation_passed = self.validate_output()
            
            self.log("\nPipeline completed successfully!")
            self.log(f"Output saved to: {self.output_path}")
            
            return validation_passed
            
        except Exception as e:
            self.log(f"\n{'='*60}")
            self.log(f"ERROR: Pipeline failed!")
            self.log(f"{'='*60}")
            self.log(f"Exception: {str(e)}")
            raise
