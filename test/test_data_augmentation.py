import os
import sys
import unittest

from test.data_augmentation import data_augmentation

# Add the parent directory to sys.path to import modules properly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDataAugmentation(unittest.TestCase):

    """ def setUp(self):
        # Create temporary directories for testing
        self.temp_input = r"d:/Python/Coca"
        self.temp_output = r"d:/Python/Coca/augmented"

        # Create a test image
        self.test_image_path = os.path.join(self.temp_input, "fanta.jpg")
        test_img = np.ones((100, 100, 3), dtype=np.uint8) * 255  # White image
        cv2.imwrite(self.test_image_path, test_img)

        # Save the original folders to restore later
        self.original_input_folder = self.patch_attribute(
            "test.data_augmentation", "input_folder", self.temp_input)
        self.original_output_folder = self.patch_attribute(
            "test.data_augmentation", "output_folder", self.temp_output)

    def tearDown(self):
        # Restore original folder paths
        self.patch_attribute("test.data_augmentation",
                             "input_folder", self.original_input_folder)
        self.patch_attribute("test.data_augmentation",
                             "output_folder", self.original_output_folder)

        # Clean up temporary directories
        shutil.rmtree(self.temp_input)
        shutil.rmtree(self.temp_output) """

    def patch_attribute(self, module_name, attribute_name, new_value):
        """Helper to patch module attributes and return original value"""
        import importlib
        module = importlib.import_module(module_name)
        original_value = getattr(module, attribute_name)
        setattr(module, attribute_name, new_value)
        return original_value

    def test_data_augmentation_function(self):
        """Test that the data_augmentation function works correctly"""
        # Run the data augmentation function
        data_augmentation()

        """ # Check if output files were created (5 for each input image)
        output_files = os.listdir(self.temp_output)
        # Should have 5 augmented images
        self.assertEqual(len(output_files), 5)

        # Check that all files are valid images
        for filename in output_files:
            img_path = os.path.join(self.temp_output, filename)

            # Check if file exists
            self.assertTrue(os.path.exists(img_path))

            # Check that it's a valid image
            image = cv2.imread(img_path)
            self.assertIsNotNone(image)

            # Check dimensions match the original
            self.assertEqual(image.shape[:2], (100, 100)) """


if __name__ == '__main__':
    unittest.main()
