# CellProfiler Slurm Batch Processor

This project provides a Python script for running CellProfiler in batches using Slurm on a High-Performance Computing (HPC) cluster. It allows you to process a directory of images using a CellProfiler pipeline and distribute the processing across multiple Slurm jobs.

## Features

- Processes batches of images using CellProfiler in parallel on an HPC cluster.
- Submits Slurm batch jobs with appropriate settings for memory, time, and output.
- Organizes the output and log files in separate directories for each batch.
- Supports specifying batch size, memory requirement, output directory, and more.

## Prerequisites

- [CellProfiler](https://cellprofiler.org) installed on your system.
- A working Slurm job scheduling system.
- Python 3.x.

## Installation

1. Clone this repository to your local machine:

   ```sh
   git clone https://github.com/FelixKohlhas/cellprofiler_slurm.git
   ```

2. Navigate to the project directory:

   ```sh
   cd cellprofiler_slurm
   ```

3. Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

```sh
python process_images.py pipeline_file output_dir image_dir [--batch-size BATCH_SIZE] [--num-channels NUM_CHANNELS] [--memory MEMORY] [--log-dir LOG_DIR] [--verbose]
```

- `pipeline_file`: Path to the CellProfiler pipeline (.cppipe) file.
- `output_dir`: Parent output directory where analysis results will be saved.
- `image_dir`: Path to the directory containing input images.
- `--batch-size`: Number of images to process in each batch (default: 32).
- `--num-channels`: Number of channels in the images (default: 4).
- `--memory`: Memory requirement for the Slurm batch job (default: 16G).
- `--log-dir`: Directory for Slurm job log files (default: slurm_logs).
- `--verbose`: Print verbose information.

### Example

#### Process images
```sh
python process_images.py example_pipeline.cppipe output images --batch-size 64 --memory 32G --verbose
```

#### Merge output
```sh
python merge_output.py output merged
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.