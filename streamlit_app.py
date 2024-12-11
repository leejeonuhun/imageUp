import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO
import os

def resize_image(image, scale_factor=2):
    """
    Resize image using different interpolation methods

    :param image: PIL Image to resize
    :param scale_factor: Factor by which to scale the image
    :return: Resized PIL Image
    """
    # Convert PIL Image to numpy array
    img_array = np.array(image)

    # Get original dimensions
    height, width = img_array.shape[:2]
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # Resize using different methods
    methods = {
        'Nearest Neighbor': cv2.INTER_NEAREST,
        'Bilinear': cv2.INTER_LINEAR,
        'Bicubic': cv2.INTER_CUBIC,
        'Lanczos': cv2.INTER_LANCZOS4
    }

    resized_images = {}
    for name, method in methods.items():
        resized = cv2.resize(img_array, (new_width, new_height), interpolation=method)
        resized_images[name] = Image.fromarray(resized)

    return resized_images

def process_folder(folder_path, scale_factor):
    """
    Process all images in a folder and resize them

    :param folder_path: Path to the folder containing images
    :param scale_factor: Scale factor for resizing images
    :return: List of resized images and their filenames
    """
    supported_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
    resized_results = []

    for filename in os.listdir(folder_path):
        if any(filename.lower().endswith(ext) for ext in supported_extensions):
            file_path = os.path.join(folder_path, filename)
            try:
                original_image = Image.open(file_path)
                resized_images = resize_image(original_image, scale_factor)
                resized_results.append((filename, resized_images))
            except Exception as e:
                st.error(f"Failed to process {filename}: {e}")

    return resized_results

def main():
    st.title('🖼️ Image Resizer')

    # Sidebar for additional options
    st.sidebar.header('Resize Settings')
    scale_factor = st.sidebar.slider('Scale Factor', min_value=1.0, max_value=4.0, value=2.0, step=0.5)

    # Option to choose between file or folder upload
    st.sidebar.header('Choose Input Method')
    input_method = st.sidebar.radio('Input Method', ['File Upload', 'Folder Upload'])

    if input_method == 'File Upload':
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=['jpg', 'jpeg', 'png', 'bmp', 'webp'],
            help="Upload an image file to resize"
        )

        if uploaded_file is not None:
            # Read the image
            original_image = Image.open(uploaded_file)

            # Display original image
            st.subheader('Original Image')
            st.image(original_image, caption=f'Original Size: {original_image.size}')

            # Resize and display
            try:
                resized_images = resize_image(original_image, scale_factor)

                # Display resized images
                st.subheader(f'Resized Images (Scale: {scale_factor}x)')

                for name, img in resized_images.items():
                    st.image(img, caption=f'{name} - {img.size}')

                # Download options
                st.subheader('Download Resized Images')
                for name, img in resized_images.items():
                    # Convert image to bytes
                    byte_io = BytesIO()
                    img.save(byte_io, format='PNG')
                    byte_io.seek(0)

                    # Download button
                    st.download_button(
                        label=f'Download {name}',
                        data=byte_io,
                        file_name=f'resized_{name.lower().replace(" ", "_")}.png',
                        mime='image/png'
                    )

            except Exception as e:
                st.error(f"Error processing image: {e}")

    elif input_method == 'Folder Upload':
        # Folder path input
        folder_path = st.text_input("Enter the folder path containing images:")

        if folder_path:
            if os.path.isdir(folder_path):
                try:
                    results = process_folder(folder_path, scale_factor)

                    for filename, resized_images in results:
                        st.subheader(f'Resized Images for {filename}')
                        for name, img in resized_images.items():
                            st.image(img, caption=f'{name} - {img.size}')

                        # Download options
                        st.subheader(f'Download Resized Images for {filename}')
                        for name, img in resized_images.items():
                            # Convert image to bytes
                            byte_io = BytesIO()
                            img.save(byte_io, format='PNG')
                            byte_io.seek(0)

                            # Download button
                            st.download_button(
                                label=f'Download {filename} ({name})',
                                data=byte_io,
                                file_name=f'{filename}_resized_{name.lower().replace(" ", "_")}.png',
                                mime='image/png'
                            )

                except Exception as e:
                    st.error(f"Error processing folder: {e}")
            else:
                st.error("Invalid folder path. Please enter a valid directory.")

if __name__ == '__main__':
    main()
