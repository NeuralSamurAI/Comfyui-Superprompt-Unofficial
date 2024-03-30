SuperPrompter Node for ComfyUI

The SuperPrompter node is a ComfyUI node that uses the SuperPrompt-v1 model from Hugging Face to generate text based on a given prompt. It provides various parameters to control the text generation process.

Installation
Make sure you have ComfyUI installed. If not, follow the installation instructions from the ComfyUI documentation.

1. Create a directory named superprompter inside the ComfyUI nodes directory.
2. Place the __init__.py and superprompter_node.py files inside the superprompter directory.
3. Install the required dependencies by running the following command: pip install -r requirements.txt

Usage
1. Launch ComfyUI.
2. In the ComfyUI interface, you should see a new node called "SuperPrompter" under the "text" category.
3. Add the SuperPrompter node to your workflow.
4. Configure the input parameters:
    prompt: The prompt or starting text for generating the text.
    max_new_tokens: The maximum number of new tokens to generate.
    repetition_penalty: The penalty for repeating tokens in the generated text.
    temperature: The temperature value for controlling the randomness of the generated text.
    top_p: The cumulative probability threshold for top-p sampling.
    top_k: The number of top tokens to consider for top-k sampling.
    seed: The random seed for reproducibility. Set to 0 for random seed.
5. Connect the SuperPrompter node to other nodes in your workflow as needed.
6. Execute the workflow to generate text based on the provided prompt and parameters.

Model
The SuperPrompter node uses the SuperPrompt-v1 model from Hugging Face. The model files will be automatically downloaded and saved in the ~/.superprompter/model_files directory when the node is first used.

License
This node is released under the MIT License.

Credits
The SuperPrompter node is based on the SuperPrompt-v1 model and concept by roborovski on Hugging Face:

Original Source: https://brianfitzgerald.xyz/prompt-augmentation/
Model: [roborovski/superprompt-v1](https://huggingface.co/roborovski/superprompt-v1)
 