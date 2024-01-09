import argparse
import os
import subprocess

def get_batch_name(batch_num):
    """
    Generate the batch name for the Slurm job.

    :param batch_num: Batch number.
    :return: Batch name in the format 'batch_{batch_num}'.
    """
    return f"batch_{str(batch_num).zfill(3)}"

def submit_slurm_job(batch_name, batch_start, batch_end, pipeline_file, output_dir, image_dir, memory, log_dir, verbose):
    """
    Submit a Slurm batch job for processing a batch of images.

    :param batch_name: Name of the Slurm batch job.
    :param batch_start: Starting index of the image batch.
    :param batch_end: Ending index of the image batch.
    :param pipeline_file: Path to the CellProfiler pipeline (.cppipe) file.
    :param output_dir: Parent output directory where the analysis results will be saved.
    :param image_dir: Path to the directory containing input images.
    :param memory: Memory requirement for the Slurm batch job.
    :param log_dir: Directory for Slurm job log files.
    :param verbose: Print verbose information if True.
    """
    batch_output_dir = os.path.join(output_dir, batch_name)
    os.makedirs(batch_output_dir, exist_ok=True)

    # Construct the Slurm job submission command
    cmd = [
        "sbatch",
        f"--job-name={batch_name}",
        f"--output={os.path.join(log_dir, f'{batch_name}.log')}",
        f"--time=24:00:00",
        f"--mem={memory}",
        "--wrap",
        f'cellprofiler -c -r -p "{pipeline_file}" -f "{batch_start}" -l "{batch_end - 1}" -o "{batch_output_dir}" -i "{image_dir}"',
    ]

    if verbose:
        print(" ".join(cmd))

    # Run the Slurm job submission command
    subprocess.run(cmd, check=True)  # Add `check=True` to raise an exception if the subprocess fails

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run CellProfiler using Slurm on batches of images.")
    parser.add_argument("pipeline_file", help="Path to the CellProfiler pipeline (.cppipe) file.")
    parser.add_argument("output_dir", help="Parent output directory where the analysis results will be saved.")
    parser.add_argument("image_dir", help="Path to the directory containing input images.")
    parser.add_argument("--batch-size", type=int, default=32, help="Number of images to process in each batch.")
    parser.add_argument("--num-channels", type=int, default=4, help="Number of channels in the images.")
    parser.add_argument("--memory", default="16G", help="Memory requirement for the Slurm batch job.")
    parser.add_argument("--log-dir", default="slurm_logs", help="Directory for Slurm job log files.")
    parser.add_argument("--verbose", action="store_true", help="Print verbose information.")
    args = parser.parse_args()

    # Convert paths to absolute paths
    pipeline_file = os.path.abspath(args.pipeline_file)
    output_dir = os.path.abspath(args.output_dir)
    image_dir = os.path.abspath(args.image_dir)
    log_dir = os.path.abspath(args.log_dir)

    # Verify the pipeline_file is a valid .cppipe file
    _, extension = os.path.splitext(pipeline_file)
    if extension.lower() != ".cppipe":
        raise ValueError("Invalid pipeline file. Please provide a valid CellProfiler pipeline file with .cppipe extension.")

    # Check if the image directory exists
    if not os.path.isdir(image_dir):
        raise FileNotFoundError(f"Image directory '{image_dir}' not found. Please provide a valid image directory.")

    # Create the parent output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create the log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    image_list = os.listdir(image_dir)
    total_images = len(image_list) // args.num_channels + 1

    print(f"Total images found: {total_images}")

    # Process images in batches using Slurm
    for i in range(0, total_images, args.batch_size):
        batch_start = i
        batch_end = min(i + args.batch_size, total_images)
        batch_name = get_batch_name(i // args.batch_size + 1)

        # Submit the current batch as a Slurm job
        submit_slurm_job(
            batch_name, batch_start, batch_end, pipeline_file, output_dir, image_dir,
            args.memory, log_dir, args.verbose
        )

        if args.verbose:
            print(f"Batch {batch_name} submitted.")

    print("Batch jobs submitted to Slurm for image processing.")

if __name__ == "__main__":
    main()
