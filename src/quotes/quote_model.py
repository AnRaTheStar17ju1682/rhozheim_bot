from PIL import Image, ImageDraw, ImageFont, ImageOps
import colorsys
from io import BytesIO


class Quote:
    def __init__(
        self,
        text: str,
        name: str,
        avatar: Image.Image | None = None,
        *,
        avatar_size: int =100,
        avatar_border_size: int = 15,
        text_rect_color=(40, 40, 40),
        text_color=(255, 255, 255),
        name_color=(255, 255, 255),
        font_size=40,
        padding=25,
        bottom_padding=75,
        corner_radius=30,
        max_width=750,
        line_spacing=18,
        stroke_width = 15,
        font_path = "OpenSans.ttf",
        bold_font_path = "OpenSans-Bold.ttf"
    ):
        self.text = text
        self.name = name
        self.avatar = avatar
        
        self.avatar_size = avatar_size
        self.avatar_border_size = avatar_border_size
        self.bordered_avatar_size = avatar_size + avatar_border_size
        self.text_rect_color = text_rect_color
        self.text_color = text_color
        self.name_color = name_color
        self.font_size = font_size
        self.padding = padding
        self.bottom_padding = bottom_padding
        self.corner_radius = corner_radius
        self.max_width = max_width
        self.line_spacing = line_spacing
        self.stroke_width = stroke_width
        self.font_path = font_path
        self.bold_font_path = bold_font_path
        
        self.text_font = ImageFont.truetype(font_path, self.font_size)
        self.name_font = ImageFont.truetype(bold_font_path, self.font_size*1.1)
        self.text_size_test_probe = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        
        if not self.avatar:
            self.avatar = self.generate_avatar(background_color=name_color)
        self._process_avatar()
    
    
    def generate_avatar(self, background_color=(173, 216, 230)):
        image = Image.new('RGB', (self.avatar_size, self.avatar_size), background_color)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.bold_font_path, self.avatar_size // 2)
        letter = self.name[0].upper()

        text_width, text_height = self._text_size_in_pixels(letter, font)
        position = ((self.avatar_size - text_width) // 2, (self.avatar_size - text_height) // 4)
        
        draw.text(position, letter, font=font, fill=(255, 255, 255))
        
        return image
    
    
    def _process_avatar(self):
        if self.avatar.mode != 'RGBA':
            self.avatar = self.avatar.convert('RGBA')
        
        avatar = ImageOps.fit(self.avatar, (self.avatar_size, self.avatar_size), method=Image.BICUBIC)
        bordered_avatar = Image.new('RGBA', (self.bordered_avatar_size, self.bordered_avatar_size), (0, 0, 0, 0))
        self._put_avatar_to_border(bordered_avatar, avatar)
        self._add_rainbow_border_to_avatar(bordered_avatar)
        
        self.avatar = bordered_avatar
    
    
    def _put_avatar_to_border(self, bordered_avatar: Image.Image, avatar: Image.Image) -> None:
        avatar_mask = Image.new("L", (self.avatar_size, self.avatar_size), 0)
        ImageDraw.Draw(avatar_mask).ellipse((0, 0, self.avatar_size, self.avatar_size), fill=255)
        avatar.putalpha(avatar_mask)
        bordered_avatar.paste(avatar, (self.avatar_border_size//2, self.avatar_border_size//2))
    
    
    def _add_rainbow_border_to_avatar(self, bordered_avatar: Image.Image):
        num_segments = 12
        segment_angle = 360 / num_segments
        
        for i in range(num_segments):
            hue = i / num_segments
            r, g, b = colorsys.hsv_to_rgb(hue, 0.4, 0.9)
            ImageDraw.Draw(bordered_avatar).arc(
                [
                    -self.avatar_border_size //2,
                    -self.avatar_border_size //2,
                    self.bordered_avatar_size+self.avatar_border_size //2,
                    self.bordered_avatar_size+self.avatar_border_size //2],
                start=int(i * segment_angle),
                end=int((i+1) * segment_angle),
                fill=(int(r*255), int(g*255), int(b*255), 150),
                width=self.avatar_border_size +2
            )
        
        mask = Image.new("L", (self.bordered_avatar_size, self.bordered_avatar_size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, self.bordered_avatar_size, self.bordered_avatar_size), fill=255)
        bordered_avatar.putalpha(mask)
    
    
    @property
    def quote_image(self) -> BytesIO:
        text_rect_image, text_rect_width, text_rect_height = self._process_text()
        image_width = self.bordered_avatar_size + self.padding + text_rect_width
        image_height = text_rect_height + self.bottom_padding
        
        quote_image = Image.new('RGBA', (image_width, image_height + self.bottom_padding), (0, 0, 0, 0))  # Добавили доп. место
        quote_image.paste(self.avatar, (0, 0+self.padding//2))
        quote_image.paste(text_rect_image, (0 + self.bordered_avatar_size + self.padding, 0))
        
        buffer = BytesIO()
        quote_image.save(buffer, "WEBP")
        
        return buffer
    
    
    # DONT LOOK AT ME
    def _process_text(self) -> Image.Image:
        name_height = self._text_size_in_pixels(self.name, self.name_font)[1] + self.padding//2
        text_rect_width = self.max_width - self.bordered_avatar_size
        text_area_width = text_rect_width - self.padding*2
        lines = self._split_text_to_lines(text_area_width, self.text)
        line_height = self._text_size_in_pixels("A", self.text_font)[1]
        text_height = line_height * len(lines) + self.line_spacing * (len(lines) - 1) + self.padding
        content_width = text_rect_width + self.padding
        content_height = name_height + text_height + int(self.padding*3.5)
        
        text_rect_image = Image.new('RGBA', (content_width, content_height), (0, 0, 0, 0))
        text_rect_draw = ImageDraw.Draw(text_rect_image)
        text_rect_draw.rounded_rectangle(
        [0, 0, content_width, content_height],  # Сместили для обводки
        radius=self.corner_radius,
        fill=self.text_rect_color + (255,)
        )
        
        x_text_position = self.padding
        y_text_position = self.padding
        
        text_rect_draw.text((x_text_position, y_text_position), self.name, font=self.name_font, fill=self.name_color)
        for i, line in enumerate(lines):
            y_offset = (self.padding*2 + name_height) + i * (line_height + self.line_spacing)
            text_rect_draw.text((x_text_position, y_offset), line, font=self.text_font, fill=self.text_color)

        
        return text_rect_image, content_width, content_height
    
    
    def _split_text_to_lines(self, text_area_width, text):
        lines = []
        current_line = ""
        
        def _split_word(word):
            parts = []
            remaining = word
            while remaining:
                remaining_width = self._text_size_in_pixels(remaining, self.text_font)[0]
                if remaining_width <= text_area_width:
                    parts.append(remaining)
                    break
                else:
                    for split_pos in range(len(remaining)-1, 0, -1):
                        candidate = remaining[:split_pos]
                        candidate_width, _ = self._text_size_in_pixels(candidate, self.text_font)
                        if candidate_width <= text_area_width:
                            break
                    parts.append(remaining[:split_pos])
                    remaining = remaining[split_pos:]
            return parts
        
        for word in text.split():
            test_line = f"{current_line} {word}".strip() if current_line else word
            test_width = self._text_size_in_pixels(test_line, self.text_font)[0]
            
            if test_width <= text_area_width:
                current_line = test_line
            else:
                # if "current line" is not empty string and not the first "if",
                # that means the string fits, but without the word
                if current_line:
                    lines.append(current_line)
                    current_line = ""
                # check that a word lesser than a sting
                if self._text_size_in_pixels(word, self.text_font)[0] <= text_area_width:
                    current_line = word
                else:
                    parts = _split_word(word)
                    if parts:
                        lines.extend(parts[:-1])
                        current_line = parts[-1]
                        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    
    def _text_size_in_pixels(self, text, font):
        bbox = self.text_size_test_probe.textbbox((0, 0), text, font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]