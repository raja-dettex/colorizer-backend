from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)

import torch

if not torch.cuda.is_available():
    print('GPU not available.')

import fastai
from deoldify.visualize import *
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")
print('set warning')




from deoldify.visualize import get_image_colorizer
from deoldify.generators import gen_inference_deep


# Define a modified load function for Learner that sets weights_only=False
def modified_learner_load(self, name:PathOrStr, device:torch.device=None, strict:bool=True):
    """Load model and optimizer state (from `name`) depending on `device`.

    Modified to use weights_only=False for torch.load.
    """
    # Ensure device is set, default to data.device if available
    if device is None:
        device = self.data.device if hasattr(self, 'data') and hasattr(self.data, 'device') else None
    if device is None:
        # Fallback if data or data.device is not available on the learner
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


    # Get the path to the model weights
    model_path = self.path/self.model_dir/f'{name}.pth'

    # Check if the model file exists
    if not model_path.exists():
         raise FileNotFoundError(f"Model file not found at {model_path}")


    print(f"Loading model from {model_path} with weights_only=False...")
    try:
        # Use torch.load with weights_only=False - REMOVED pickle_open_args
        state = torch.load(model_path, map_location=device)
        print("Model state loaded successfully.")
    except Exception as e:
        print(f"Error during torch.load: {e}")
        # Re-raise the exception after printing
        raise

    # Load the model state dictionary
    if 'model' in state:
        print("Loading model state_dict from 'model' key...")
        self.model.load_state_dict(state['model'], strict=strict)
        print("Model state_dict loaded.")
    elif 'model_state_dict' in state:
        # Sometimes the key is 'model_state_dict'
        print("Loading model state_dict from 'model_state_dict' key...")
        self.model.load_state_dict(state['model_state_dict'], strict=strict)
        print("Model state_dict loaded.")
    else:
        # If neither 'model' nor 'model_state_dict' key is present, assume the state_dict is the state itself
        print("Loading model state_dict directly from loaded state...")
        self.model.load_state_dict(state, strict=strict)
        print("Model state_dict loaded.")


    # Load optimizer state if present
    if 'optimizer' in state and hasattr(self.opt, 'load_state_dict'):
        print("Loading optimizer state_dict...")
        try:
            self.opt.load_state_dict(state['optimizer'])
            print("Optimizer state_dict loaded.")
        except Exception as e:
             print(f"Warning: Could not load optimizer state_dict: {e}")


# Store the original Learner.load method
original_learner_load = Learner.load

# Temporarily replace the Learner's load method with our modified version
Learner.load = modified_learner_load

try:
    # Now call get_image_colorizer.
    # This will internally create a Learner and call its load method,
    # which is now our modified version that uses weights_only=False.
    print("Calling get_image_colorizer...")
    colorizer = get_image_colorizer(artistic=True)
    print("get_image_colorizer finished.")
except Exception as e:
    print(f"\nAn error occurred during colorizer initialization: {e}")
finally:
    # IMPORTANT: Restore the original Learner.load method
    # This prevents unintended side effects in other parts of your notebook
    # or future uses of fastai's Learner.
    print("Restoring original Learner.load method.")
    Learner.load = original_learner_load

# After this block runs, if no error occurred within the try block,
# the 'colorizer' variable should be initialized and ready to use.

if 'colorizer' in locals() and colorizer is not None:
    print("\nColorizer initialized successfully!")
else:
    print("\nColorizer initialization failed. Check the error message above for details.")