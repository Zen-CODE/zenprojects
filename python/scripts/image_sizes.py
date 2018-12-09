from os.path import join, isdir
from os import listdir
import PIL.Image as PILImage


class ImageSize(object):
    """
    Class managing image sizes.
    """
    exts = [".png", ".jpg"]

    def gen_size_file(self, folder, out_file):
        """Generate a file containing the image sizes.
        """
        sizes = []  # A list contained name and size tuples

        files = listdir(folder)
        for item in files:
            for ext in ImageSize.exts:
                if item.endswith(ext):
                    sizes.append((item, self.get_size(join(folder, item))))

        self.write_to_file(sizes, out_file)

    @staticmethod
    def write_to_file(name_size_list, out_file):
        """ Write the name and size into the to specified file. """
        with open(out_file, 'wb') as f:
            for name, size in name_size_list:
                f.write(str(name + " " + str(size) + "\n").encode('utf-8'))


    @staticmethod
    def get_size(img_path):
        """ Return the tuple containing the width and height of the image"""
        with PILImage.open(img_path) as img:
            return img.size


if __name__ == "__main__":
    # Initialize
    ImageSize().gen_size_file(
        '/home/fruitbat/Repos/kivy-speedtest/graphics/',
        '/home/fruitbat/Repos/kivy-speedtest/graphics/sizes.txt')

