import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO  # 추가된 부분

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

def main():
    st.title('🖼️ Image Resizer')
    
    # Sidebar for additional options
    st.sidebar.header('Resize Settings')
    scale_factor = st.sidebar.slider('Scale Factor', min_value=1.0, max_value=4.0, value=2.0, step=0.5)
    
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
        col1, col2 = st.columns(2)
        with col1:
            st.image(original_image, caption=f'Original Size: {original_image.size}')
        
        # Resize and display
        try:
            resized_images = resize_image(original_image, scale_factor)
            
            # Display resized images
            st.subheader(f'Resized Images (Scale: {scale_factor}x)')
            
            # Create columns for each resize method
            cols = st.columns(2)
            
            # Display resized images in columns
            method_names = list(resized_images.keys())
            for i, (name, img) in enumerate(resized_images.items()):
                with cols[i % 2]:
                    st.image(img, caption=f'{name} - {img.size}')
            
            # Download options
            st.subheader('Download Resized Images')
            download_col = st.columns(len(resized_images))
            
            for i, (name, img) in enumerate(resized_images.items()):
                with download_col[i]:
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

if __name__ == '__main__':
    main()
