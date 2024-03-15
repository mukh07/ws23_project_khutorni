from PIL import Image


def calculate_new_size(original_size, requested_size, keep_aspect_ratio=True):
    if not keep_aspect_ratio:
        return requested_size

    width, height = original_size
    aspect_ratio = width / height
    max_width, max_height = requested_size
    if width > height:
        new_width = max_width
        new_height = int(new_width / aspect_ratio)
        if new_height > max_height:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
    else:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)
        if new_width > max_width:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)

    return new_width, new_height


def resize_image(image, size, keep_aspect_ratio=True,
                 pad=True, pad_color=(0, 0, 0)):
    new_width, new_height = calculate_new_size(
        image.size, size, keep_aspect_ratio)
    resized_image = image.resize((new_width, new_height))

    if pad:
        padded_image = Image.new('RGB', size, pad_color)
        padded_image.paste(resized_image, ((size[0] - new_width) // 2, 
                                           (size[1] - new_height) // 2))
        return padded_image

    return resized_image
