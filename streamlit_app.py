import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

def resize_image(image, scale_factor=2):
    """
    Resize image using different interpolation methods

    :param image: PIL Image to resize
    :param scale_factor: Factor by which to scale the image
    :return: Resized PIL Image
    """
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

def main():
    st.title('🖼️ Image Resizer with Multiple File Upload')

    # Sidebar for additional options
    st.sidebar.header('Resize Settings')
    scale_factor = st.sidebar.slider('Scale Factor', min_value=1.0, max_value=4.0, value=2.0, step=0.5)

    # File uploader for multiple files
    uploaded_files = st.file_uploader(
        "Upload multiple image files",
        type=['jpg', 'jpeg', 'png', 'bmp', 'webp'],
        accept_multiple_files=True,
        help="Select multiple image files to resize"
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                # Read the image
                original_image = Image.open(uploaded_file)

                # Display original image
                st.subheader(f'Original Image: {uploaded_file.name}')
                st.image(original_image, caption=f'Original Size: {original_image.size}')

                # Resize and display
                resized_images = resize_image(original_image, scale_factor)

                # Display resized images
                st.subheader(f'Resized Images for {uploaded_file.name} (Scale: {scale_factor}x)')
                for name, img in resized_images.items():
                    st.image(img, caption=f'{name} - {img.size}')

                # Download options
                st.subheader(f'Download Resized Images for {uploaded_file.name}')
                for name, img in resized_images.items():
                    # Convert image to bytes
                    byte_io = BytesIO()
                    img.save(byte_io, format='PNG')
                    byte_io.seek(0)

                    st.download_button(
                        label=f'Download {name}',
                        data=byte_io,
                        file_name=f'{uploaded_file.name.split(".")[0]}_resized_{name.lower().replace(" ", "_")}.png',
                        mime='image/png'
                    )

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")

if __name__ == '__main__':
    main()
