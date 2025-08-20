# Parabricks: GPU-Accelerated Genomics, Ready for Local (WSL) and Cloud

Genomic data volumes have exploded, but the *time* to turn raw reads into actionable variants no longer has to. **NVIDIA Parabricks** is a free software suite that accelerates secondary analysis of NGS DNA and RNA data—bringing end-to-end whole-genome workflows down from many hours on CPUs to minutes on GPUs, with outputs concordant to widely used tools. For example, Parabricks can analyze a 30× human whole genome in roughly **\~10 minutes** on modern GPUs while matching the accuracy of trusted CPU pipelines. ([NVIDIA Docs][1])

This repository, **`gabenavarro/parabricks`**, provides a practical, developer-friendly scaffold to run Parabricks:

* **Locally on Windows** via **WSL2 + Docker** (great for day-to-day development and benchmarking), leveraging Microsoft’s and NVIDIA’s official CUDA-on-WSL enablement and the NVIDIA Container Toolkit. ([Microsoft Learn][2], [NVIDIA Docs][3])
* **In the cloud** on major providers (AWS/GCP/Azure), using GPU instances and ready-to-adapt examples and notebooks for reproducible runs and cost/perf benchmarking. ([Amazon Web Services, Inc.][4], [NVIDIA Docs][5])

---

## Why Parabricks matters (a short history)

* **From the Human Genome Project to today.** The first human genome cost hundreds of millions to sequence and took years; sustained technological progress since the mid-2000s made high-coverage genomes routine and pushed costs down orders of magnitude, enabling population-scale studies—but also overwhelming CPU-bound analysis pipelines. ([Genome.gov][6])
* **The CPU era of secondary analysis.** Tools like **BWA** for short-read alignment and **GATK HaplotypeCaller** for variant calling became the de facto standards, but their throughput on general-purpose CPUs often meant *hours to days* per sample at 30× coverage. ([PubMed][7], [Oxford Academic][8], [GATK][9])
* **GPU acceleration arrives.** In 2019–2020, **Parabricks** joined NVIDIA and rapidly expanded GPU-accelerated implementations of common workflows (germline, somatic, RNA-seq, long-reads), shrinking WGS turnaround from day-scale to **minutes** and making high-volume genomics more affordable. ([Frost Brown Todd][10], [NVIDIA Developer][11])

---

## What Parabricks accelerates

Parabricks provides GPU-optimized versions (and turnkey workflows) of widely adopted steps—e.g., BWA-MEM alignment, GATK Best Practices (BQSR, MarkDuplicates, HaplotypeCaller), DeepVariant, somatic callers, and increasingly long-read and pangenome/graph workflows. With current H100-class hardware, complete germline pipelines can finish in the **10–15 minute** range under benchmark conditions. ([NVIDIA Docs][12], [NVIDIA Developer][13])

Accuracy remains central: outputs are designed to **match** the canonical CPU tools, simplifying validation and mixed-infrastructure deployments. ([NVIDIA Docs][1])

---

## Benchmarking and ground truth

For method checks and performance tracking, the field commonly relies on **Genome in a Bottle (GIAB)** reference materials (e.g., HG001/NA12878, HG002/NA24385) and associated benchmark regions and truth sets. This repo uses those datasets and conventions to help you reproduce *both* speedups and accuracy. ([NIST][14], [NIST][15])

* Example public indices and pointers to GIAB FASTQs/BAMs are maintained by NIST/NCBI and collaborators, making it straightforward to pull 30× WGS data for tests. ([GitHub][16])

---

## Local (WSL2) + Docker: developer-friendly by design

Windows developers can enjoy native-like Linux GPU acceleration through **WSL2**. Follow the official guidance to enable CUDA for WSL and install the **NVIDIA Container Toolkit**; then, GPU-aware Docker containers can run Parabricks commands (`pbrun …`) directly inside your WSL distro. This repo’s README and scripts consolidate those steps. ([Microsoft Learn][2], [NVIDIA Docs][3])

---

## Cloud-ready for scale

Whether you prefer managed marketplace images or DIY container workflows, cloud providers offer GPU instances well-suited for Parabricks. NVIDIA and partners provide step-by-step guides and AMIs; our notebooks mirror those patterns and add cost/performance notes so you can right-size instances for your throughput and budget. ([Amazon Web Services, Inc.][4], [NVIDIA Docs][5])

---

## What’s in this repo

* **WSL2 + Docker quickstart** for local development (with VS Code tips). ([Microsoft Learn][2], [NVIDIA Docs][17])
* **Benchmark recipes** for:

  * **Transcriptomics (RNA-seq)**: STAR/GATK-based flow on public datasets.
  * **30× WGS germline**: GIAB HG00x datasets + concordance checks vs. CPU baselines. ([NIST][14])
* **Cloud notebooks/guides**: launch, run, and teardown patterns on AWS/GCP, with pointers to official docs and AMIs. ([Amazon Web Services, Inc.][4], [NVIDIA Docs][5])

---

## Learn more (authoritative references)

* **Parabricks overview & docs** (features, runtimes, workflows). ([NVIDIA Docs][1])
* **Canonical CPU tools**: BWA (Li & Durbin) and GATK HaplotypeCaller. ([PubMed][7], [Oxford Academic][8], [GATK][9])
* **Historical context**: sequencing costs and scale (NHGRI). ([Genome.gov][6])
* **Parabricks + NVIDIA** (history and speedups). ([NVIDIA Developer][11])
* **WSL2 GPU enablement & container runtime**. ([Microsoft Learn][2], [NVIDIA Docs][3])
* **Cloud how-tos** (AWS/GCP examples). ([Amazon Web Services, Inc.][4], [NVIDIA Docs][5])

---

> **Goal of `gabenavarro/parabricks`:** make it trivial for you (and collaborators) to reproduce fast, concordant Parabricks results **locally** on Windows via WSL2 *and* **at scale** in the cloud—complete with datasets, benchmarks, and DevEx niceties that reduce toil and maximize throughput.

[1]: https://docs.nvidia.com/clara/parabricks/4.5.1/Overview.html "Overview"
[2]: https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl "Enable NVIDIA CUDA on WSL 2"
[3]: https://docs.nvidia.com/cuda/wsl-user-guide/index.html "CUDA on WSL User Guide"
[4]: https://aws.amazon.com/blogs/hpc/benchmarking-the-nvidia-clara-parabricks-germline-pipeline-on-aws/ "Benchmarking the NVIDIA Clara Parabricks germline ..."
[5]: https://docs.nvidia.com/clara/parabricks/latest/Tutorials/CloudGuides/AWS.html "Running NVIDIA Parabricks on AWS"
[6]: https://www.genome.gov/about-genomics/fact-sheets/Sequencing-Human-Genome-cost "The Cost of Sequencing a Human Genome"
[7]: https://pubmed.ncbi.nlm.nih.gov/19451168/ "Fast and accurate short read alignment with Burrows- ..."
[8]: https://academic.oup.com/bioinformatics/article/25/14/1754/225615 "Fast and accurate short read alignment with Burrows–Wheeler ..."
[9]: https://gatk.broadinstitute.org/hc/en-us/articles/360037225632-HaplotypeCaller "HaplotypeCaller – GATK - Genome Analysis Toolkit"
[10]: https://frostbrowntodd.com/case-study-cross-practice-team-assists-with-nvidia-parabricks-acquisition/ "Case study: Cross-practice team assists with NVIDIA/ ..."
[11]: https://developer.nvidia.com/blog/advancing-dna-sequencing/ "NVIDIA Parabricks: Accelerating Genomic Analysis from ..."
[12]: https://docs.nvidia.com/clara/parabricks/latest/welcome-to-nvidia-parabricks-v4-3-1.1.pdf "Welcome to NVIDIA Parabricks v4.3.1"
[13]: https://developer.nvidia.com/blog/accelerate-genomic-analysis-for-any-sequencer-with-parabricks-v4-2/ "Accelerate Genomic Analysis for Any Sequencer with ..."
[14]: https://www.nist.gov/programs-projects/genome-bottle "Genome in a Bottle"
[15]: https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=924178 "Reproducible integration of multiple sequencing datasets to form high- ..."
[16]: https://github.com/genome-in-a-bottle/giab_data_indexes "genome-in-a-bottle/giab_data_indexes"
[17]: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html "Installing the NVIDIA Container Toolkit"
