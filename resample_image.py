import SimpleITK as sitk
import numpy as np
import os

def resample_image(image_path, output_path, is_label, spacing_x, spacing_y, spacing_z, size_x, size_y, size_z):
    """
    Resample a given image to a specified voxel spacing and dimensions.
    
    :param image_path: Path to the input image (.nii.gz)
    :param output_path: Path to save the resampled image
    :param is_label: Boolean indicating if the image is a label (True) or not (False)
    :param spacing_x: Spacing along axis 0
    :param spacing_y: Spacing along axis 1
    :param spacing_z: Spacing along axis 2
    :param size_x: Desired size along axis 0
    :param size_y: Desired size along axis 1
    :param size_z: Desired size along axis 2
    """
    # Define interpolation method and default pixel value based on label type
    interpolator = sitk.sitkNearestNeighbor if is_label else sitk.sitkBSpline
    default_pixel_value = 0 if is_label else -1024
    
    # Read image
    image = sitk.ReadImage(image_path)
    new_spacing = (spacing_x, spacing_y, spacing_z)
    new_size = (size_x, size_y, size_z)
    
    # Resample image
    resample = sitk.ResampleImageFilter()
    resample.SetReferenceImage(image)
    resample.SetSize(new_size)
    resample.SetDefaultPixelValue(default_pixel_value)
    resample.SetInterpolator(interpolator)
    resample.SetOutputDirection(image.GetDirection())
    resample.SetOutputOrigin(image.GetOrigin())
    resample.SetOutputSpacing(new_spacing)
    
    resampled_image = resample.Execute(image)
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save resampled image
    sitk.WriteImage(resampled_image, output_path, useCompression=True)
    print(f"{os.path.basename(image_path)} resampled and saved to {output_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", type=str, help="Path to the input image")
    parser.add_argument("output_path", type=str, help="Path to save the resampled image")
    parser.add_argument("--is_label", action="store_true", help="Specify if the image is a mask")
    parser.add_argument("--spacing_x", type=float, required=True, help="Spacing x")
    parser.add_argument("--spacing_y", type=float, required=True, help="Spacing y")
    parser.add_argument("--spacing_z", type=float, required=True, help="Spacing z")
    parser.add_argument("--size_x", type=int, required=True, help="Dimention x")
    parser.add_argument("--size_y", type=int, required=True, help="Dimention y")
    parser.add_argument("--size_z", type=int, required=True, help="Dimention z")
    
    args = parser.parse_args()
    
    resample_image(
        args.image_path,
        args.output_path,
        args.is_label,
        args.spacing_x,
        args.spacing_y,
        args.spacing_z,
        args.size_x,
        args.size_y,
        args.size_z
    )
