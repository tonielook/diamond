import xml.dom.minidom
import numpy as np
import os
from PIL import Image, ImageDraw
from shutil import copy2


def checkXML(filelist):
    status = None
    for f in filelist:
        if f.split('.')[-1] == 'xml':
            status = f
    return status


def GenMask_inclusion(src_folder,xmlfile,save_folder):
    # categorys = {'Crystal':0, 'Cloud':1, 'Pinpoint':2, 'Feather':3, 'Twinning_wisp':4, 'Needle':5}
    # corresponding color for types of inclusions
    colors = {'Pinpoint':(255,0,0), 'Crystal':(0,255,0), 'Needle':(0,0,255), 
              'Cloud':(255,0,0), 'Twinning_wisp':(0,255,0), 'Feather':(0,0,255),
              'Internal_graining':(255,0,0)}

    mask1 = ['Pinpoint', 'Crystal', 'Needle']
    mask2 = ['Cloud', 'Twinning_wisp', 'Feather']
    mask3 = ['Internal_graining']
    
    dom = xml.dom.minidom.parse(os.path.join(src_folder,xmlfile))
    xml_root = dom.documentElement
    images = xml_root.getElementsByTagName('image')
    
    for ii in range(len(images)):
        t = images[ii]
        t_width = int(t.getAttribute("width"))
        t_height = int(t.getAttribute("height"))
        t_name = t.getAttribute("name").split('/')[-1]
        
        img_mask1 = Image.new('RGB', (int(t_width), int(t_height)))
        draw1 = ImageDraw.Draw(img_mask1)
        img_mask2 = Image.new('RGB', (int(t_width), int(t_height)))
        draw2 = ImageDraw.Draw(img_mask2)
        img_mask3 = Image.new('RGB', (int(t_width), int(t_height)))
        draw3 = ImageDraw.Draw(img_mask3)
        
        t_poly = t.getElementsByTagName("polygon") + t.getElementsByTagName("polyline")
        for t_ply in t_poly:
            t_ply_points = t_ply.getAttribute("points")
            t_ply_points = t_ply_points.split(";")
            t_ply_points = np.asarray([[int(float(b)) for b in a.split(",")] for a in t_ply_points])
            t_x = t_ply_points[:,0]
            t_y = t_ply_points[:,1]
            t_xy = [(x,y) for x,y in zip(t_x,t_y)]
            t_ply_label = t_ply.getAttribute("label").split('_')[0]

            if t_ply_label in mask1:
                draw1.polygon(t_xy, fill=colors[t_ply_label])
            elif t_ply_label in mask2:
                draw2.polygon(t_xy, fill=colors[t_ply_label])
            elif t_ply_label in mask3:
                draw3.polygon(t_xy, fill=colors[t_ply_label])

        img_mask1.save(os.path.join(save_folder, t_name[:11]+'_mask1.png'))
        img_mask2.save(os.path.join(save_folder, t_name[:11]+'_mask2.png'))
        img_mask3.save(os.path.join(save_folder, t_name[:11]+'_mask3.png'))
    
        # save original image
        try:
            img_name = [n for n in os.listdir(src_folder) if t_name[:11] in n and 'png' in n][0]
            copy2(os.path.join(src_folder,img_name),os.path.join(save_folder,t_name[:11]+'.png'))
        except:
            img_name = [n for n in os.listdir(os.path.join(src_folder,'Twinning wisp')) if t_name[:11] in n and 'png' in n][0]
            copy2(os.path.join(src_folder,img_name),os.path.join(save_folder,t_name[:11]+'.png'))

        print(t_name[:11] + ' saved ...')


def GenMask_inclusion_reflection(src_folder,xmlfile,mask_save_folder, img_save_folder, is_index=False,fontsize=5):
    # corresponding color for inclusion and reflection
    # inclusion = (255,0,0), reflection = (0,255,0)
    dom = xml.dom.minidom.parse(xmlfile)
    xml_root = dom.documentElement
    images = xml_root.getElementsByTagName('image')
    
    for ii in range(len(images)):
        t = images[ii]
        t_width = int(t.getAttribute("width"))
        t_height = int(t.getAttribute("height"))
        t_name = t.getAttribute("name").split('/')[-1]
        
        img_mask = Image.new('RGB', (int(t_width), int(t_height)))
        draw = ImageDraw.Draw(img_mask)
        
        t_poly = t.getElementsByTagName("polygon") + t.getElementsByTagName("polyline")
        for t_ply in t_poly:
            t_ply_points = t_ply.getAttribute("points")
            t_ply_points = t_ply_points.split(";")
            t_ply_points = np.asarray([[int(float(b)) for b in a.split(",")] for a in t_ply_points])
            t_x = t_ply_points[:,0]
            t_y = t_ply_points[:,1]
            t_xy = [(x,y) for x,y in zip(t_x,t_y)]
            t_ply_label = t_ply.getAttribute("label")
            
            if 'Internal_graining' not in t_ply_label:

                if not 'Reflection' in t_ply_label:
                    draw.polygon(t_xy, fill=(0,255,0))
                else:
                    draw.polygon(t_xy, fill=(255,0,0))
        
        img_mask.save(os.path.join(mask_save_folder, t_name[:11]+'_mask.png'))
        
        # save original image
        try:
            img_name = [n for n in os.listdir(src_folder) if t_name[:11] in n and 'png' in n][0]
            copy2(os.path.join(src_folder,img_name),os.path.join(img_save_folder,t_name[:11]+'.png'))
        except:
            img_name = [n for n in os.listdir(os.path.join(src_folder,'Twinning wisp')) if t_name[:11] in n and 'png' in n][0]
            copy2(os.path.join(src_folder,'Twinning wisp',img_name),os.path.join(img_save_folder,t_name[:11]+'.png'))

        print(t_name[:11] + ' saved ...')



def main():

    src_folder = r'../data_input'
    save_folder = r'../data_output/1_Masks'
    img_save_folder = r'../data_output/1_Images'
    os.makedirs(save_folder, exist_ok=True)
    os.makedirs(img_save_folder, exist_ok=True)
    
    for root,dirs,files in os.walk(src_folder):
        status = checkXML(files)
        if status is not None:
            print(root)
            xmlfile = os.path.join(root,status)
            print(xmlfile)
            # R=reflection, G=inclusion
            GenMask_inclusion_reflection(root,xmlfile,save_folder,img_save_folder,is_index=False,fontsize=5)


if __name__ == "__main__":
	main()


