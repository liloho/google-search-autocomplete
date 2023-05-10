import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib import font_manager

#load custom fonts
letter_font = font_manager.FontProperties(fname='assets/fonts/Take cover.ttf')
subtitle_font = font_manager.FontProperties(fname='assets/fonts/Inter-Medium.ttf')
label_font = font_manager.FontProperties(fname='assets/fonts/OpenSans-Regular.ttf')

#add line break when printing long prompts
def format_prompt_for_plot(prompt):
    num_spaces = prompt.count(" ")
    
    if (len(prompt) > 10) & (num_spaces==1):            
        ind = prompt.find(" ")
        prompt_print = prompt[:ind] + "\n"+ prompt[ind+1:]
    elif  (len(prompt) > 10) & (num_spaces>1):
        ind = prompt.find(" ", prompt.find(" ") + 1)
        prompt_print = prompt[:ind] + "\n"+ prompt[ind+1:]
    else:
        prompt_print = prompt
    return prompt_print

# === LAYOUTS

# circular outward
def plot_circular_outward(data_for_plot, prompt, bg_colour, font_colour, line_colour):
    
    df = data_for_plot
    prompt_print = format_prompt_for_plot(prompt)

    #== Inputs
    # chart dimensions
    fig,ax = plt.subplots(figsize=(15, 11), layout="tight")
    height = 26         
    width = 10

    fig.set_facecolor(bg_colour)
    
    # calculate offet
    array = np.linspace(0, 1*np.pi, height)
    offset = [round(x,2)for x in np.sin(array)*2.5]
    
    #positions for letters on a straight line with circular offset
    df["x_pos"] = [width + i for i in offset]
    df["y_pos"] = [26 - i for i in range(len(df))]
    
    #== Data
    center_x, center_y = (5, (height-1)/2+1)  # center of circle
    
    indent=5
    for i in range(len(df)):
        x_pos = df["x_pos"].iloc[i] 
        y_pos = df["y_pos"].iloc[i] 
        
        #lines from center point outwards using Bezier curve
        verts = [(center_x, center_y), (center_x +indent*1.2, center_y), (center_x -indent*0.2, center_y), (x_pos, y_pos)] 
        codes = [Path.MOVETO] + [Path.CURVE4] * 3
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor='none', lw=1, edgecolor=line_colour)
        ax.add_patch(patch)
        
        #plot letter
        ax.text(x_pos , y_pos,df["letter"].iloc[i] , va="center",ha="center",
               fontsize=24, fontproperties=letter_font,color=font_colour,
               bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.0'))
        
        #plot text
        ax.text(x_pos+0.3 , y_pos, df["result"].iloc[i].replace(prompt.lower() + " ", "") , va="center",ha="left",
               fontsize=15, fontproperties=subtitle_font, color=font_colour)
    
    #configure axes
    ax.set_ylim(-1, height+1)
    ax.set_xlim(-1, width+5)
    ax.axis("off")
    
    #=====
    #Title and footer
    ax.text(center_x -0.3, center_y, prompt_print , va="center",ha="right",
               fontsize=50, fontproperties=letter_font, color=font_colour)
    ax.text(center_x -0.3, center_y-5,"Google autocomplete\nsuggestions" , va="center",ha="right",
               fontsize=15, fontproperties=subtitle_font, color=font_colour)

    if sum(data_for_plot["result"].str.find("*")) != -26:
        ax.text(center_x -0.3, center_y-7, "*no relevant results", fontproperties= label_font, fontsize=12,  ha="right", color=font_colour)
    
    return fig