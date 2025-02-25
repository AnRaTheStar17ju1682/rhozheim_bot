from PIL import Image
from io import BytesIO


class Track:
    def __init__(self, title: str, audio: bytes, thumbnail: bytes):
        self.title = title
        self.audio = audio
        self.thumbnail = thumbnail
        self._crop_image()
    
    
    def _crop_image(self) -> None:
        img = Image.open(BytesIO(self.thumbnail))
        
        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        
        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.thumbnail(size=(300,300))
        jpeg_buffer = self._image_to_jpeg(cropped_img)
        
        self.thumbnail = jpeg_buffer.getvalue()
    
    
    def _image_to_jpeg(self, img: Image.Image) -> BytesIO:
        jpeg_buffer = BytesIO()
        
        img.save(jpeg_buffer, format='JPEG', quality=70)
        
        return jpeg_buffer