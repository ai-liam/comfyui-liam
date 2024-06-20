import sys
import os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

sys.path.append(path+"/../../")

import img_nodes
from .text_nodes import SaveText, MergeText,DisplayText
from .Audio import SpeechRecognition, SpeechSynthesis
from .llm_ai_store import AiStoreAzureGPTNode
from .llm_ollama import OllamaApiTNode
#sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))


NODE_CLASS_MAPPINGS = {
    "LiamLibLoadImage": img_nodes.LoadImage,
    "LiamLibImageToGray": img_nodes.ImageToGray,
    "LiamLibSaveImg": img_nodes.MySaveImage,
    "LiamLibFillImage": img_nodes.FillImage ,
    "PreviewReliefImage": img_nodes.PreviewReliefImage ,
    "GetBetterDepthImage": img_nodes.GetBetterDepthImage ,

    "LiamLibSaveText": SaveText ,
    "LiamLibMergeText": MergeText ,
    "LiamLibDisplayText": DisplayText ,

    "SpeechRecognitionLiam": SpeechRecognition,
    "SpeechSynthesisLiam": SpeechSynthesis,
    "AiStoreAzureGPTLiam": AiStoreAzureGPTNode,
    "OllamaApiTNodeLiam": OllamaApiTNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LiamLibLoadImage": "Load Image @Liam",
    "LiamLibImageToGray": "Image To Gray @Liam",
    "LiamLibSaveImg": "Save Image @Liam",
    "LiamLibFillImage":  "Fill Image @Liam",
    "PreviewReliefImage": "Preview Relief Image @Liam",
    "GetBetterDepthImage":  "Get Better Depth Image @Liam",

    "LiamLibSaveText": "Save Text @Liam",
    "LiamLibMergeText": "Merge Text @Liam",
    "LiamLibDisplayText": "Display Text @Liam",

    "SpeechRecognitionLiam": "SpeechRecognition @Liam",
    "SpeechSynthesisLiam": "SpeechSynthesis @Liam",
    "AiStoreAzureGPTLiam": "AiStoreAzureGPT @Liam",
    "OllamaApiTNodeLiam": "OllamaApiChat @Liam",
}
