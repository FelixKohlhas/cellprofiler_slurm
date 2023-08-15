# Image Processing with CellProfiler and Slurm

This Python script facilitates batch image processing using CellProfiler and Slurm, a job scheduling system. It enables the efficient processing of a large number of images by distributing the workload across multiple batches, leveraging the power of a computing cluster.

## Features

- Process batches of images using CellProfiler with Slurm job scheduling.
- Automatically generate batch names based on batch numbers.
- Verbose mode for detailed output and monitoring.
- Configurable batch size and memory requirements.

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
python merge_output.py output/* merged/
```

## Contributing

Contributions are welcome! If you have any improvements, bug fixes, or new features to add, please follow these steps:

1. Fork this repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note:** This README provides a general overview of the project. Please refer to the source code and inline comments for more detailed information.