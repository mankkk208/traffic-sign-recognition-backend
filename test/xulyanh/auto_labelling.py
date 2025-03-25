from autodistill.detection import CaptionOntology
from autodistill_grounded_sam import GroundedSAM

# define an ontology to map class names to our GroundingDINO prompt
# the ontology dictionary has the format {caption: class}
# where caption is the prompt sent to the base model, and class is the label that will
# be saved for that caption in the generated annotations
base_model = GroundedSAM(ontology=CaptionOntology({"drinks": "fanta"}))

# label all images in a folder called `context_images`
base_model.label(
    input_folder=r"C:\Users\Lenovo\Desktop\BienBao",
    output_folder=r"C:\Users\Lenovo\Desktop\autolabels",
)