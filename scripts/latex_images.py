# Redefining the latex_to_image function and then testing it

import matplotlib.pyplot as plt
import os

def latex_to_image(latex_str, directory="/Users/mattmurphy/Thermodynamics/src/gui/widgets/images"):
    """
    Convert a LaTeX string to an image using matplotlib.
    
    Parameters:
    - latex_str (str): The LaTeX string to be converted.
    - directory (str): Directory where the image will be saved.

    Returns:
    - str: Path to the saved image.
    """

    # Modify matplotlib rcParams for font settings
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['text.usetex'] = False

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Generate a filename based on the LaTeX string content
    filename = "".join([c if c.isalnum() else "_" for c in latex_str]) + ".png"
    output_path = os.path.join(directory, filename)

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(5, 5))

    # Set the background color
    ax.set_facecolor('#990000')
    fig.set_facecolor('#990000')

    # Render the LaTeX string in the center of the axis with the specified style
    ax.text(0.5, 0.5, f"${latex_str}$", size=110, ha='center', va='center', 
            color='#FFFFFF', weight='bold')

    # Hide the axis and set limits
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Save the image
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(output_path, format="png", bbox_inches="tight", pad_inches=0.1, dpi=300, facecolor=fig.get_facecolor())
    plt.close(fig)
    
    return output_path

# Testing the function
latex_string = "\phi^V"
output_path = latex_to_image(latex_str=latex_string)
print(output_path)
