# beit_model.py
import torch
import timm
from PIL import Image
from torchvision import transforms

# 1. This is the complete and correct list of your 221 class names.
CLASS_NAMES = ['Men_Mojaris', 'Men__Accessory_Gift_Set', 'Men__Backpacks', 'Men__Bangle', 'Men__Belts', 'Men__Blazers', 'Men__Boxers', 'Men__Bracelet', 'Men__Briefs', 'Men__Caps', 'Men__Casual_Shoes', 'Men__Churidar', 'Men__Cufflinks', 'Men__Deodorant', 'Men__Duffel_Bag', 'Men__Flip_Flops', 'Men__Formal_Shoes', 'Men__Fragrance_Gift_Set', 'Men__Free_Gifts', 'Men__Gloves', 'Men__Handbags', 'Men__Innerwear_Vests', 'Men__Jackets', 'Men__Jeans', 'Men__Kurtas', 'Men__Kurtis', 'Men__Laptop_Bag', 'Men__Lounge_Pants', 'Men__Lounge_Shorts', 'Men__Messenger_Bag', 'Men__Mufflers', 'Men__Nehru_Jackets', 'Men__Night_suits', 'Men__Pendant', 'Men__Perfume_and_Body_Mist', 'Men__Rain_Jacket', 'Men__Rain_Trousers', 'Men__Ring', 'Men__Sandals', 'Men__Scarves', 'Men__Shirts', 'Men__Shoe_Accessories', 'Men__Shorts', 'Men__Socks', 'Men__Sports_Sandals', 'Men__Sports_Shoes', 'Men__Stoles', 'Men__Sunglasses', 'Men__Suspenders', 'Men__Sweaters', 'Men__Sweatshirts', 'Men__Ties', 'Men__Track_Pants', 'Men__Tracksuits', 'Men__Trousers', 'Men__Trunk', 'Men__Tshirts', 'Men__Waistcoat', 'Men__Wallets', 'Men__Watches', 'Men__Water_Bottle', 'Men_dhoti-pants', 'Men_kurta', 'Men_nehru-jackets', 'Men_sherwanis', 'Unisex__Backpacks', 'Unisex__Basketballs', 'Unisex__Belts', 'Unisex__Caps', 'Unisex__Casual_Shoes', 'Unisex__Deodorant', 'Unisex__Duffel_Bag', 'Unisex__Flip_Flops', 'Unisex__Footballs', 'Unisex__Free_Gifts', 'Unisex__Hair_Colour', 'Unisex__Handbags', 'Unisex__Hat', 'Unisex__Headband', 'Unisex__Jeans', 'Unisex__Key_chain', 'Unisex__Laptop_Bag', 'Unisex__Messenger_Bag', 'Unisex__Mobile_Pouch', 'Unisex__Perfume_and_Body_Mist', 'Unisex__Rain_Jacket', 'Unisex__Rucksacks', 'Unisex__Sandals', 'Unisex__Scarves', 'Unisex__Shoe_Accessories', 'Unisex__Socks', 'Unisex__Sports_Sandals', 'Unisex__Sports_Shoes', 'Unisex__Sunglasses', 'Unisex__Swimwear', 'Unisex__Tablet_Sleeve', 'Unisex__Travel_Accessory', 'Unisex__Trolley_Bag', 'Unisex__Tshirts', 'Unisex__Waist_Pouch', 'Unisex__Wallets', 'Unisex__Watches', 'Unisex__Water_Bottle', 'Unisex__Wristbands', 'Women _leggings-&-salwars', 'Women_Mojaris', 'Women__Baby_Dolls', 'Women__Backpacks', 'Women__Bangle', 'Women__Bath_Robe', 'Women__Beauty_Accessory', 'Women__Belts', 'Women__Blazers', 'Women__Body_Lotion', 'Women__Bra', 'Women__Bracelet', 'Women__Briefs', 'Women__Camisoles', 'Women__Capris', 'Women__Caps', 'Women__Casual_Shoes', 'Women__Churidar', 'Women__Clutches', 'Women__Compact', 'Women__Concealer', 'Women__Deodorant', 'Women__Dresses', 'Women__Duffel_Bag', 'Women__Dupatta', 'Women__Earrings', 'Women__Eye_Cream', 'Women__Eyeshadow', 'Women__Face_Moisturisers', 'Women__Face_Scrub_and_Exfoliator', 'Women__Face_Serum_and_Gel', 'Women__Face_Wash_and_Cleanser', 'Women__Flats', 'Women__Flip_Flops', 'Women__Foundation_and_Primer', 'Women__Fragrance_Gift_Set', 'Women__Free_Gifts', 'Women__Hair_Colour', 'Women__Handbags', 'Women__Heels', 'Women__Highlighter_and_Blush', 'Women__Jackets', 'Women__Jeans', 'Women__Jeggings', 'Women__Jewellery_Set', 'Women__Jumpsuit', 'Women__Kajal_and_Eyeliner', 'Women__Kurta_Sets', 'Women__Kurtas', 'Women__Kurtis', 'Women__Laptop_Bag', 'Women__Leggings', 'Women__Lehenga_Choli', 'Women__Lip_Care', 'Women__Lip_Gloss', 'Women__Lip_Liner', 'Women__Lip_Plumper', 'Women__Lipstick', 'Women__Lounge_Pants', 'Women__Lounge_Shorts', 'Women__Lounge_Tshirts', 'Women__Makeup_Remover', 'Women__Mascara', 'Women__Mask_and_Peel', 'Women__Mobile_Pouch', 'Women__Mufflers', 'Women__Nail_Essentials', 'Women__Nail_Polish', 'Women__Necklace_and_Chains', 'Women__Night_suits', 'Women__Nightdress', 'Women__Patiala', 'Women__Pendant', 'Women__Perfume_and_Body_Mist', 'Women__Ring', 'Women__Robe', 'Women__Salwar', 'Women__Salwar_and_Dupatta', 'Women__Sandals', 'Women__Sarees', 'Women__Scarves', 'Women__Shapewear', 'Women__Shirts', 'Women__Shorts', 'Women__Shrug', 'Women__Skirts', 'Women__Socks', 'Women__Sports_Sandals', 'Women__Sports_Shoes', 'Women__Stockings', 'Women__Stoles', 'Women__Sunglasses', 'Women__Sunscreen', 'Women__Sweaters', 'Women__Sweatshirts', 'Women__Swimwear', 'Women__Ties_and_Cufflinks', 'Women__Tights', 'Women__Toner', 'Women__Tops', 'Women__Track_Pants', 'Women__Travel_Accessory', 'Women__Trousers', 'Women__Tshirts', 'Women__Tunics', 'Women__Umbrellas', 'Women__Waistcoat', 'Women__Wallets', 'Women__Watches', 'Women_blouse', 'Women_dupattas', 'Women_gowns', 'Women_kurti-long', 'Women_lehenga', 'Women_palazzos', 'Women_petticoats', 'Women_saree']
model_architecture = 'beit_base_patch16_224'

# 2. Define the image transformations
# These should be the same as the validation transformations from your training script
data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 3. Load the model and set to evaluation mode
device = torch.device("cpu") # Use "cuda" if you have a GPU
model = timm.create_model(model_architecture, pretrained=False, num_classes=len(CLASS_NAMES))
model.load_state_dict(torch.load('epoch_12.pth', map_location=device))
model.to(device)
model.eval()

def run_beit_classification(image: Image.Image) -> str:
    """
    Takes a single cropped PIL image, preprocesses it, and returns its 
    predicted class label as a string.
    """
    # Ensure the image is in RGB format
    if image.mode != 'RGB':
        image = image.convert('RGB')
        
    # Apply the transformations and add a batch dimension (B, C, H, W)
    transformed_image = data_transforms(image).unsqueeze(0)
    transformed_image = transformed_image.to(device)

    # Perform inference
    with torch.no_grad():
        output = model(transformed_image)
    
    # Get the predicted class index by finding the max logit
    _, predicted_idx = torch.max(output, 1)
    
    # Map the index to the class name
    class_label = CLASS_NAMES[predicted_idx.item()]
    
    return class_label
