import streamlit as st
from PIL import Image
import zipfile
from io import BytesIO

def upscale_to_4k(image):
    # Define the resolution for 4K
    target_width = 3840
    target_height = 2160
    original_width, original_height = image.size

    # Calculate new dimensions while maintaining aspect ratio
    aspect_ratio = original_width / original_height
    if aspect_ratio > 1:  # Landscape
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:  # Portrait or square
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    return image.resize((new_width, new_height), Image.LANCZOS)

def main():
    st.title("Batch Image Upscaling to 4K")
    st.write("Upload up to 20 images, and this app will upscale each to 4K resolution without distortion.")

    # Upload multiple images
    uploaded_files = st.file_uploader(
        "Choose up to 20 images", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True, 
        key="uploaded_files"
    )

    if uploaded_files and len(uploaded_files) <= 20:
        # Store upscaled images
        upscaled_images = []
        image_counter = 1  # Counter for unique naming

        # Display original images
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Original Image: {uploaded_file.name}", use_container_width=True)

        # Convert all images to 4K
        if st.button("Convert All to 4K"):
            with st.spinner("Upscaling all images..."):
                for uploaded_file in uploaded_files:
                    image = Image.open(uploaded_file)
                    upscale_image = upscale_to_4k(image)

                    # Generate a unique name for the upscaled image
                    original_name = uploaded_file.name
                    name_without_ext = original_name.rsplit('.', 1)[0]
                    upscaled_name = f"{name_without_ext}_4k_{image_counter}.png"
                    image_counter += 1

                    # Save upscaled image in memory with its unique name
                    upscaled_images.append((upscaled_name, upscale_image))
                st.success("All images have been upscaled to 4K!")

        # Provide download options if images have been converted
        if upscaled_images:
            # Create and download a ZIP file of all images
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for name, image in upscaled_images:
                    # Save each image into the ZIP file
                    img_buffer = BytesIO()
                    image.save(img_buffer, format="PNG")
                    zip_file.writestr(name, img_buffer.getvalue())

            zip_buffer.seek(0)  # Reset buffer position for reading

            if st.download_button(
                label="Download All 4K Images (ZIP)",
                data=zip_buffer,
                file_name="upscaled_images_4k.zip",
                mime="application/zip"
            ):
                # Rerun the app to clear everything after download
                st.experimental_rerun()

    elif uploaded_files:
        st.error("You can upload a maximum of 20 images. Please reduce the number of images.")

if __name__ == "__main__":
    main()
