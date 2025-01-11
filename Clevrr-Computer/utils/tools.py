from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import tool

from utils.contants import MODELS

from PIL import Image, ImageDraw, ImageFont
import pyautogui as pg
import base64

pg.PAUSE = 2

def get_ruled_screenshot():

    image = pg.screenshot()
    # Get the image dimensions
    width, height = image.size

    # Create a new image for the semi-transparent layer
    overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))  # Transparent layer
    draw = ImageDraw.Draw(overlay)

    # Set the line color (gray) and line opacity (adjusting the alpha value)
    line_color = (200, 200, 0, 128)  # The last value (128) controls opacity, 0 = fully transparent, 255 = fully opaque

    # Load a font for the labels (you can specify any TTF font you have)
    try:
        font = ImageFont.truetype("arial.ttf", 25)
    except IOError:
        font = ImageFont.load_default()

    # Draw vertical and horizontal lines every 100 pixels and add labels
    for x in range(0, width, 50):
        draw.line([(x, 0), (x, height)], fill=line_color, width=1)
        # Add labels at the top for vertical lines
        if x % 100 == 0:
            draw.text((x + 5, 5), str(x), font=font, fill=(250, 250, 0, 128))
            draw.text((x, height - 25), str(x), font=font, fill=(250, 250, 0, 128))

    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=line_color, width=1)
        # Add labels on the left for horizontal lines
        if y % 100 == 0:
            draw.text((5, y + 5), str(y), font=font, fill=(0, 250, 250, 128))
            text_width, text_height = 35, 15
            draw.text((width - text_width - 5, y + 5), str(y), font=font, fill=(0, 250, 250, 128))

    # Convert screenshot to RGBA for proper merging
    image = image.convert("RGBA")

    # Merge the overlay (with lines and labels) back onto the original image
    combined = Image.alpha_composite(image.convert("RGBA"), overlay)
    combined.save("screenshot.png")

    from langchain.pydantic_v1 import BaseModel, Field

class ScreenInfo(BaseModel):
    query: str = Field(description="should be a question about the screenshot of the current screen. Should always be in text.")

@tool(args_schema=ScreenInfo)
def get_screen_info(question: str) -> dict:
    """Tool to get the information about the current screen on the basis of the question of the user. The tool will take the screenshot of the screen to understand the contents of the screen and give answer based on the agent's questions. Do not write code to take screenshot."""
    try:
        get_ruled_screenshot()
        with open(f"screenshot.png", "rb") as image:
            image = base64.b64encode(image.read()).decode("utf-8")
            messages = [
                SystemMessage(
                content="""You are a Computer agent that is responsible for answering questions based on the input provided to you. You will have access to the screenshot of the current screen of the user along with a grid marked with true coordinates of the screen. The size of the screen is 1920 x 1080 px.
                        ONLY rely on the coordinates marked in the screen. DO NOT create an assumption of the coordinates. 
                        Here's how you can help:
                        1. Find out coordinates of a specific thing. You have to be super specific about the coordinates. These coordinates will be passed to PyAutoGUI Agent to perform further tasks. Refer the grid line to get the accurate coordinates.
                        2. Give information on the contents of the screen.
                        3. Analyse the screen to give instructions to perform further steps.
                        
                    """
                ),
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": f"{question}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image}"}
                        }
                    ]
                )
            ]
            image_model = MODELS["gemini"]
            response = image_model.invoke(messages)
            return response.content
        
    except Exception as e:
        return {"error": str(e)}
