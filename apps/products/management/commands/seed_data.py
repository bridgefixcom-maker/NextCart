import os
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from apps.products.models import Category, Product, ProductImage


CATEGORIES = [
    {'name': 'Fruits',              'slug': 'fruits'},
    {'name': 'Vegetables',          'slug': 'vegetables'},
    {'name': 'Dairy & Eggs',        'slug': 'dairy-eggs'},
    {'name': 'Beverages',           'slug': 'beverages'},
    {'name': 'Snacks',              'slug': 'snacks'},
    {'name': 'Bakery',              'slug': 'bakery'},
    {'name': 'Rice & Grains',       'slug': 'rice-grains'},
    {'name': 'Pulses & Lentils',    'slug': 'pulses-lentils'},
    {'name': 'Spices & Masala',     'slug': 'spices-masala'},
    {'name': 'Oils & Ghee',         'slug': 'oils-ghee'},
    {'name': 'Noodles & Pasta',     'slug': 'noodles-pasta'},
    {'name': 'Sauces & Condiments', 'slug': 'sauces-condiments'},
    {'name': 'Frozen Foods',        'slug': 'frozen-foods'},
    {'name': 'Meat & Seafood',      'slug': 'meat-seafood'},
    {'name': 'Breakfast Cereals',   'slug': 'breakfast-cereals'},
    {'name': 'Ice Cream & Desserts','slug': 'ice-cream-desserts'},
    {'name': 'Chocolates & Sweets', 'slug': 'chocolates-sweets'},
    {'name': 'Personal Care',       'slug': 'personal-care'},
    {'name': 'Household Cleaning',  'slug': 'household-cleaning'},
    {'name': 'Baby Products',       'slug': 'baby-products'},
    {'name': 'Organic & Natural',   'slug': 'organic-natural'},
    {'name': 'Pet Food',            'slug': 'pet-food'},
]

# Image pools per category — products cycle through these
IMG = {
    'fruits': [
        'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1547514701-42782101795e?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1563114773-84221bd62daa?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1587132137056-bfbf0166836e?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1528825871115-3581a5387919?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400&h=400&fit=crop',
    ],
    'vegetables': [
        'https://images.unsplash.com/photo-1524593166156-312f362cada0?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1447175008436-054170c2e979?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1622205313162-be1d5712a43f?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1583692331507-fc0bd348695d?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=400&h=400&fit=crop',
    ],
    'dairy-eggs': [
        'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1599599811977-9c9a344d90a8?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1552767059-ce182ead6c1b?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1587252537745-cd14a4b3cdb0?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=400&fit=crop',
    ],
    'beverages': [
        'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1536064479547-7ee40b74b807?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400&h=400&fit=crop',
    ],
    'snacks': [
        'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1575324285701-e6dba6c4ea94?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1551248429-40975aa4de74?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1607920591413-4ec007e70023?w=400&h=400&fit=crop',
    ],
    'bakery': [
        'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1558401391-7899b4bd5bbf?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1550617931-e17a7b70dce2?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1519915028121-7d3463d20b13?w=400&h=400&fit=crop',
    ],
    'rice-grains': [
        'https://images.unsplash.com/photo-1536304993881-ff86e0c9c24e?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1548069011-f5a0750f5c7a?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1551462147-ff29053bfc14?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop',
    ],
    'pulses-lentils': [
        'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1556909212-d5b11f8fc1e3?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1612367541113-2be8a4d5a4b2?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1491555103944-7c647fd857e6?w=400&h=400&fit=crop',
    ],
    'spices-masala': [
        'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1599909533290-c2fa1a0a6c6b?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1532336414038-cf19250c5757?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1506368249639-73a05d6f6488?w=400&h=400&fit=crop',
    ],
    'oils-ghee': [
        'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1631704824503-1ef3cc25a22b?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1620656798579-1984d9e87df7?w=400&h=400&fit=crop',
    ],
    'noodles-pasta': [
        'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1551183053-bf91798d773e?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1555126634-323283e090fa?w=400&h=400&fit=crop',
    ],
    'sauces-condiments': [
        'https://images.unsplash.com/photo-1472476443507-c7a5948772fc?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1604152135912-04a022e23696?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=400&fit=crop',
    ],
    'frozen-foods': [
        'https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1619480653748-00e5a6b0e0c4?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=400&fit=crop',
    ],
    'meat-seafood': [
        'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1619881590738-a111d176d906?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1562802378-063ec186a863?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=400&h=400&fit=crop',
    ],
    'breakfast-cereals': [
        'https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1551462147-ff29053bfc14?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1607196270049-9b7fb7c2c7b5?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=400&h=400&fit=crop',
    ],
    'ice-cream-desserts': [
        'https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1516054575922-f0b8eeadec1a?w=400&h=400&fit=crop',
    ],
    'chocolates-sweets': [
        'https://images.unsplash.com/photo-1511381939415-e44015466834?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1548907040-4baa42d10919?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1575377222312-dd1a63a51638?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1606312619070-d48b4c652a52?w=400&h=400&fit=crop',
    ],
    'personal-care': [
        'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1619451683084-3f0a02a1ed49?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=400&h=400&fit=crop',
    ],
    'household-cleaning': [
        'https://images.unsplash.com/photo-1563453392212-326f5e854473?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400&h=400&fit=crop',
    ],
    'baby-products': [
        'https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1491013516836-7db643ee125a?w=400&h=400&fit=crop',
    ],
    'organic-natural': [
        'https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1542838132-92c53300491e?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1488459716781-31db52582fe9?w=400&h=400&fit=crop',
    ],
    'pet-food': [
        'https://images.unsplash.com/photo-1601758174476-72459a84c9ee?w=400&h=400&fit=crop',
        'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=400&fit=crop',
    ],
}

# (name, category_slug, price, sale_price, stock, description)
PRODUCTS = [
    # ── FRUITS (12) ──────────────────────────────────────────────────────────
    ('Red Apples (1 kg)',        'fruits',     120,  99,  50, 'Fresh red apples, sweet and crunchy. Rich in fiber and vitamins.'),
    ('Bananas (1 dozen)',        'fruits',      60,  None, 80, 'Fresh ripe bananas. Great source of potassium and natural energy.'),
    ('Alphonso Mangoes (1 kg)', 'fruits',     280, 249,  30, 'Premium Alphonso mangoes from Ratnagiri. The king of fruits.'),
    ('Oranges (1 kg)',           'fruits',     100,  None, 60, 'Juicy fresh oranges. Packed with Vitamin C.'),
    ('Green Grapes (500 g)',     'fruits',      90,   79,  45, 'Fresh seedless green grapes. Sweet and refreshing.'),
    ('Watermelon (1 pc)',        'fruits',      80,  None, 30, 'Fresh whole watermelon. Perfect summer fruit.'),
    ('Strawberries (250 g)',     'fruits',     160, 139,  25, 'Fresh ripe strawberries. Perfect for desserts and smoothies.'),
    ('Pineapple (1 pc)',         'fruits',      70,  None, 40, 'Sweet ripe pineapple. Rich in vitamin C and bromelain.'),
    ('Lemon (500 g)',            'fruits',      40,  None, 90, 'Fresh lemons. Essential for cooking and drinks.'),
    ('Papaya (1 kg)',            'fruits',      60,   49,  50, 'Fresh ripe papaya. Great for digestion.'),
    ('Pomegranate (1 kg)',       'fruits',     180, 159,  35, 'Fresh red pomegranate. Rich in antioxidants.'),
    ('Kiwi (6 pcs)',             'fruits',     120,  99,  40, 'Fresh New Zealand kiwi. Packed with Vitamin C and K.'),

    # ── VEGETABLES (15) ──────────────────────────────────────────────────────
    ('Tomatoes (1 kg)',          'vegetables',  40,  None,100, 'Farm fresh red tomatoes. Essential for Indian cooking.'),
    ('Onions (1 kg)',            'vegetables',  35,  None,120, 'Fresh onions. The base of every great Indian dish.'),
    ('Potatoes (1 kg)',          'vegetables',  30,  None,150, 'Fresh potatoes. Versatile vegetable for any dish.'),
    ('Spinach (250 g)',          'vegetables',  25,  None, 60, 'Fresh green spinach leaves. Rich in iron and vitamins.'),
    ('Carrots (500 g)',          'vegetables',  35,   29,  70, 'Fresh orange carrots. Rich in beta-carotene.'),
    ('Capsicum (500 g)',         'vegetables',  55,   45,  50, 'Colorful fresh capsicums. Great for stir fry.'),
    ('Broccoli (500 g)',         'vegetables',  70,   59,  40, 'Fresh green broccoli. High in protein and vitamins.'),
    ('Cauliflower (1 pc)',       'vegetables',  45,  None, 55, 'Fresh cauliflower. Perfect for aloo gobi.'),
    ('Cucumber (500 g)',         'vegetables',  30,  None, 80, 'Fresh cucumbers. Great for salads and raita.'),
    ('Mushrooms (200 g)',        'vegetables',  65,   55,  45, 'Fresh button mushrooms. Perfect for curries and soups.'),
    ('Sweet Corn (2 pcs)',       'vegetables',  40,  None, 70, 'Fresh sweet corn. Great for snacking and cooking.'),
    ('Peas (500 g)',             'vegetables',  55,   45,  60, 'Fresh green peas. Perfect for pulao and curries.'),
    ('Eggplant / Brinjal (1 kg)','vegetables', 40,  None, 75, 'Fresh eggplant. Great for bharta and curries.'),
    ('Lady Finger / Okra (500 g)','vegetables', 45,  None, 65, 'Fresh okra. Essential for sambar and stir fry.'),
    ('Bitter Gourd (500 g)',     'vegetables',  35,  None, 50, 'Fresh bitter gourd. Excellent for blood sugar control.'),

    # ── DAIRY & EGGS (10) ────────────────────────────────────────────────────
    ('Full Cream Milk (1 L)',    'dairy-eggs',  65,  None,200, 'Fresh full cream milk. Rich in calcium and protein.'),
    ('Toned Milk (1 L)',         'dairy-eggs',  55,  None,180, 'Fresh toned milk. Low fat, high protein.'),
    ('Amul Butter (500 g)',      'dairy-eggs', 270,  249,  80, 'Pure pasteurized cream butter.'),
    ('Fresh Paneer (200 g)',     'dairy-eggs',  90,   79,  60, 'Soft and creamy paneer. Great for curries.'),
    ('Dahi / Curd (400 g)',      'dairy-eggs',  55,  None,100, 'Fresh set curd. Probiotic rich.'),
    ('Cheese Slices (200 g)',    'dairy-eggs', 145,  129,  50, 'Processed cheese slices. Perfect for sandwiches.'),
    ('Eggs (12 pcs)',            'dairy-eggs',  80,  None,150, 'Farm fresh eggs. Rich in protein.'),
    ('Fresh Cream (200 ml)',     'dairy-eggs',  65,   55,  70, 'Fresh cream. Perfect for desserts and gravies.'),
    ('Ghee (500 ml)',            'dairy-eggs', 320,  299,  60, 'Pure cow ghee. Traditional and aromatic.'),
    ('Flavoured Yogurt (200 g)', 'dairy-eggs',  45,  None, 90, 'Creamy flavoured yogurt. Available in mango and strawberry.'),

    # ── BEVERAGES (10) ───────────────────────────────────────────────────────
    ('Tropicana Orange (1 L)',   'beverages',  110,   89,  70, 'Fresh orange juice with real fruit goodness.'),
    ('Coca Cola (2 L)',          'beverages',   95,  None, 90, 'Classic Coca-Cola. Chilled and refreshing.'),
    ('Green Tea (25 bags)',      'beverages',  185,  159,  55, 'Premium green tea bags. Rich in antioxidants.'),
    ('Coconut Water (500 ml)',   'beverages',   50,  None, 80, 'Natural fresh coconut water. Best natural electrolyte.'),
    ('Nescafe Classic (200 g)',  'beverages',  390,  349,  45, 'Rich and aromatic instant coffee.'),
    ('Real Mango Juice (1 L)',   'beverages',   95,   79,  65, 'Refreshing mango juice with real pulp.'),
    ('Sprite (2 L)',             'beverages',   90,  None, 85, 'Crisp lemon-lime flavoured soda.'),
    ('Minute Maid Lemon (300 ml)','beverages',  35,  None,100, 'Refreshing lemon drink. Perfect for hot days.'),
    ('Bournvita (500 g)',        'beverages',  265,  239,  50, 'Chocolate malt health drink. Great for kids.'),
    ('Mineral Water (1 L)',      'beverages',   20,  None,200, 'Pure mineral water. BIS certified.'),

    # ── SNACKS (10) ──────────────────────────────────────────────────────────
    ('Lays Classic (100 g)',     'snacks',      30,  None,150, 'Crispy salted potato chips. Classic flavor.'),
    ('Digestive Biscuits',       'snacks',      55,   49,  90, 'Whole wheat digestive biscuits. Healthy snacking.'),
    ('Mixed Nuts (200 g)',       'snacks',     280,  249,  40, 'Premium cashews, almonds, and raisins.'),
    ('Maggi Noodles (4 pack)',   'snacks',      68,  None,120, '2-minute Maggi masala noodles.'),
    ('Popcorn Butter (100 g)',   'snacks',      50,   39,  80, 'Light and crunchy buttered popcorn.'),
    ('Kurkure Masala (90 g)',    'snacks',      25,  None,160, 'Crunchy and spicy Indian snack.'),
    ('Bingo Mad Angles (90 g)', 'snacks',      30,  None,140, 'Triangular corn snack with tangy flavour.'),
    ('Almonds (250 g)',          'snacks',     320,  289,  45, 'Premium California almonds. Healthy and crunchy.'),
    ('Cashews (250 g)',          'snacks',     350,  319,  40, 'Premium whole cashews. Rich and buttery taste.'),
    ('Granola Bar (6 pack)',     'snacks',     180,  149,  60, 'Healthy oats and nut granola bars. Great energy boost.'),

    # ── BAKERY (9) ───────────────────────────────────────────────────────────
    ('Whole Wheat Bread',        'bakery',      45,  None,100, 'Freshly baked whole wheat bread. Soft and nutritious.'),
    ('Butter Croissant',         'bakery',      35,  None, 60, 'Flaky buttery croissant. Freshly baked every morning.'),
    ('Chocolate Cake (500 g)',   'bakery',     350,  299,  25, 'Rich moist chocolate cake. Perfect for celebrations.'),
    ('Blueberry Muffin (2 pcs)', 'bakery',      90,   75,  40, 'Soft muffins loaded with blueberries.'),
    ('Glazed Donuts (4 pcs)',    'bakery',     120,   99,  35, 'Soft and fluffy glazed donuts.'),
    ('Pav (8 pcs)',              'bakery',      30,  None, 90, 'Soft dinner rolls. Perfect with bhaji.'),
    ('Brown Bread',              'bakery',      50,  None, 80, 'Healthy brown bread. Rich in fiber.'),
    ('Multigrain Bread',         'bakery',      60,   52,  70, 'Nutritious multigrain bread. Great for sandwiches.'),
    ('Vanilla Cupcakes (4 pcs)', 'bakery',     140,  119,  30, 'Soft vanilla cupcakes with cream frosting.'),

    # ── RICE & GRAINS (8) ────────────────────────────────────────────────────
    ('Basmati Rice (5 kg)',      'rice-grains', 450, 399,  60, 'Premium long grain basmati rice. Aromatic and fluffy.'),
    ('Sona Masoori Rice (5 kg)','rice-grains', 340, 299,  70, 'Popular South Indian rice variety. Light and digestible.'),
    ('Wheat Flour Atta (5 kg)', 'rice-grains', 230, 209,  80, 'Chakki fresh whole wheat atta. Soft rotis guaranteed.'),
    ('Rolled Oats (500 g)',      'rice-grains',  95,   79,  65, 'Quick cook rolled oats. Perfect healthy breakfast.'),
    ('Poha / Flattened Rice (500 g)','rice-grains', 55, None, 90, 'Thin flattened rice. Perfect for quick breakfast.'),
    ('Suji / Semolina (500 g)', 'rice-grains',  45,  None,100, 'Fine semolina. Great for halwa, upma and idli.'),
    ('Broken Wheat Dalia (500 g)','rice-grains', 60, None, 75, 'Nutritious broken wheat. High in fiber.'),
    ('Corn Flour (500 g)',       'rice-grains',  55,  None, 85, 'Fine corn flour. Great for soups and frying.'),

    # ── PULSES & LENTILS (10) ────────────────────────────────────────────────
    ('Toor Dal (1 kg)',          'pulses-lentils', 140, 119, 80, 'Yellow pigeon peas. Essential for sambar and dal fry.'),
    ('Moong Dal (1 kg)',         'pulses-lentils', 130, None, 75, 'Yellow moong lentils. Light and easy to digest.'),
    ('Masoor Dal (1 kg)',        'pulses-lentils', 120, 99,  80, 'Red lentils. Quick cooking and nutritious.'),
    ('Chana Dal (1 kg)',         'pulses-lentils', 110, None, 85, 'Split chickpeas. Perfect for dal and snacks.'),
    ('Kabuli Chana (1 kg)',      'pulses-lentils', 130, 109, 70, 'White chickpeas. Great for chole and hummus.'),
    ('Rajma / Kidney Beans (1 kg)','pulses-lentils', 140, 119, 65, 'Red kidney beans. Perfect for rajma chawal.'),
    ('Black Urad Dal (1 kg)',    'pulses-lentils', 160, None, 60, 'Black lentils. Essential for dal makhani.'),
    ('Green Moong (1 kg)',       'pulses-lentils', 120, None, 70, 'Whole green moong beans. Nutritious and versatile.'),
    ('Moth Beans (1 kg)',        'pulses-lentils', 100, None, 55, 'High protein moth beans. Perfect for sprouts.'),
    ('Lobia / Black Eyed Peas (1 kg)','pulses-lentils', 110, 89, 60, 'Black eyed peas. Nutritious and tasty.'),

    # ── SPICES & MASALA (10) ─────────────────────────────────────────────────
    ('Turmeric Powder (200 g)',  'spices-masala',  55, None,120, 'Pure haldi powder. Anti-inflammatory properties.'),
    ('Red Chilli Powder (200 g)','spices-masala',  65,  55, 110, 'Hot red chilli powder. Adds heat to any dish.'),
    ('Coriander Powder (200 g)','spices-masala',   50, None,115, 'Aromatic dhania powder. Essential Indian spice.'),
    ('Cumin Seeds (100 g)',      'spices-masala',   45, None,130, 'Whole jeera seeds. Adds earthy flavor.'),
    ('Garam Masala (100 g)',     'spices-masala',   80,  69, 100, 'Aromatic blend of spices. Must-have for Indian cooking.'),
    ('Kitchen King Masala (100 g)','spices-masala', 75,  65,  90, 'All-purpose vegetable masala. Rich and flavorful.'),
    ('Chana Masala (100 g)',     'spices-masala',   70,  59,  85, 'Special spice blend for chole. Authentic taste.'),
    ('Black Pepper (100 g)',     'spices-masala',   95,  79,  80, 'Whole black pepper. Adds warmth and depth.'),
    ('Cardamom (50 g)',          'spices-masala',  180, 159,  60, 'Green cardamom pods. Sweet and aromatic.'),
    ('Mustard Seeds (100 g)',    'spices-masala',   35, None,140, 'Black mustard seeds. Essential for tempering.'),

    # ── OILS & GHEE (7) ──────────────────────────────────────────────────────
    ('Sunflower Oil (1 L)',      'oils-ghee',   130, 115,  90, 'Light and healthy sunflower cooking oil.'),
    ('Mustard Oil (1 L)',        'oils-ghee',   155, None,  75, 'Pure cold pressed mustard oil. Traditional flavor.'),
    ('Olive Oil (500 ml)',       'oils-ghee',   450, 399,  40, 'Extra virgin olive oil. Great for salads and cooking.'),
    ('Coconut Oil (500 ml)',     'oils-ghee',   200, 179,  55, 'Pure cold pressed coconut oil. Multi-purpose.'),
    ('Cow Ghee (500 ml)',        'oils-ghee',   580, 549,  35, 'Pure cow ghee. Rich and aromatic. Bilona method.'),
    ('Rice Bran Oil (1 L)',      'oils-ghee',   145, None,  80, 'Heart healthy rice bran oil. High smoke point.'),
    ('Groundnut Oil (1 L)',      'oils-ghee',   175, 159,  65, 'Traditional groundnut oil. Rich nutty flavor.'),

    # ── NOODLES & PASTA (8) ──────────────────────────────────────────────────
    ('Maggi 2-Minute (12 pack)', 'noodles-pasta',  180, 165, 100, 'Classic Maggi masala noodles. India favourite.'),
    ('Yippee Noodles (4 pack)', 'noodles-pasta',   68, None,  90, 'Sunfeast Yippee magic masala noodles.'),
    ('Penne Pasta (500 g)',      'noodles-pasta',   85,   72,  70, 'Premium durum wheat penne. Perfect for pasta dishes.'),
    ('Spaghetti (500 g)',        'noodles-pasta',   80,  None,  65, 'Classic Italian spaghetti. Al dente perfection.'),
    ('Hakka Noodles (200 g)',    'noodles-pasta',   45,  None,  85, 'Indo-Chinese hakka noodles. Great for stir fry.'),
    ('Rice Noodles (200 g)',     'noodles-pasta',   55,   45,   70, 'Thin rice noodles. Perfect for Asian dishes.'),
    ('Macaroni (500 g)',         'noodles-pasta',   75,  None,  75, 'Classic macaroni pasta. Great for mac and cheese.'),
    ('Vermicelli / Sevai (200 g)','noodles-pasta',  30,  None, 100, 'Thin vermicelli. Perfect for kheer and upma.'),

    # ── SAUCES & CONDIMENTS (8) ──────────────────────────────────────────────
    ('Kissan Tomato Ketchup (500 g)','sauces-condiments', 95,  79, 90, 'Tangy tomato ketchup. Perfect dipping sauce.'),
    ('Maggi Hot Sauce (200 ml)', 'sauces-condiments',  65,  None, 80, 'Fiery hot sauce. Adds kick to any dish.'),
    ('Soy Sauce (200 ml)',       'sauces-condiments',  55,  None, 75, 'Dark soy sauce. Essential for Chinese cooking.'),
    ('Mayonnaise (300 g)',       'sauces-condiments', 110,   89, 70, 'Creamy eggless mayonnaise. Perfect for sandwiches.'),
    ('Green Chutney (200 g)',    'sauces-condiments',  45,  None, 85, 'Fresh coriander mint chutney. Ready to use.'),
    ('Peanut Butter (350 g)',    'sauces-condiments', 240,  199, 55, 'Creamy peanut butter. High protein spread.'),
    ('Mixed Pickle (400 g)',     'sauces-condiments',  85,   72, 80, 'Traditional mixed vegetable pickle. Tangy and spicy.'),
    ('Mango Pickle (400 g)',     'sauces-condiments',  90,  None, 75, 'Classic aam ka achaar. Traditional Indian pickle.'),

    # ── FROZEN FOODS (8) ─────────────────────────────────────────────────────
    ('Frozen Peas (500 g)',      'frozen-foods',  65,   55, 80, 'Flash frozen green peas. Retains nutrients perfectly.'),
    ('Frozen French Fries (500 g)','frozen-foods', 120,  99, 70, 'Crispy frozen french fries. Easy to make at home.'),
    ('Frozen Corn (500 g)',      'frozen-foods',  70,  None, 75, 'Sweet frozen corn kernels. Great for soups and salads.'),
    ('Frozen Paneer Tikka (250 g)','frozen-foods', 180, 155, 45, 'Ready to cook paneer tikka. Just grill and serve.'),
    ('Frozen Samosa (10 pcs)',   'frozen-foods', 130,  109, 50, 'Crispy frozen samosas. Just fry and enjoy.'),
    ('Frozen Paratha (5 pcs)',   'frozen-foods', 110,   89, 60, 'Ready to cook stuffed parathas. Aloo and gobi.'),
    ('Frozen Mixed Vegetables (500 g)','frozen-foods', 80, 69, 85, 'Mixed frozen vegetables. Great for quick cooking.'),
    ('Frozen Fish Fingers (250 g)','frozen-foods', 220, 199, 40, 'Crispy fish fingers. Ready in minutes.'),

    # ── MEAT & SEAFOOD (8) ───────────────────────────────────────────────────
    ('Fresh Chicken (1 kg)',     'meat-seafood', 220, 199, 50, 'Farm fresh broiler chicken. Cleaned and ready to cook.'),
    ('Chicken Breast (500 g)',   'meat-seafood', 180, None, 55, 'Boneless chicken breast. High protein, low fat.'),
    ('Chicken Wings (500 g)',    'meat-seafood', 170,  149, 45, 'Fresh chicken wings. Perfect for BBQ and fry.'),
    ('Rohu Fish (1 kg)',         'meat-seafood', 250, None, 35, 'Fresh rohu fish. Essential in Bengali cooking.'),
    ('Prawns (500 g)',           'meat-seafood', 380,  349, 30, 'Fresh medium prawns. Cleaned and deveined.'),
    ('Pomfret (500 g)',          'meat-seafood', 320,  299, 25, 'Fresh silver pomfret. Delicate flavour.'),
    ('Mutton (500 g)',           'meat-seafood', 450,  419, 30, 'Fresh mutton. Tender cuts for curries.'),
    ('Eggs (30 pcs)',            'meat-seafood', 200,  179, 80, 'Fresh farm eggs. Large size, protein rich.'),

    # ── BREAKFAST CEREALS (8) ────────────────────────────────────────────────
    ('Kelloggs Cornflakes (500 g)','breakfast-cereals', 230, 199, 70, 'Classic crunchy cornflakes. Great breakfast with milk.'),
    ('Muesli (500 g)',           'breakfast-cereals', 280,  249, 55, 'Fruit and nut muesli. Nutritious and filling.'),
    ('Quick Oats (500 g)',       'breakfast-cereals',  95,   79, 80, 'Rolled oats for quick cooking. High in fiber.'),
    ('Chocos (375 g)',           'breakfast-cereals', 195,  169, 60, 'Chocolate flavoured corn cereal. Kids favourite.'),
    ('Upma Mix (200 g)',         'breakfast-cereals',  45,  None, 90, 'Ready mix upma. Quick and nutritious breakfast.'),
    ('Idli Rava (500 g)',        'breakfast-cereals',  55,  None, 85, 'Fine idli rava. Perfect for soft idlis.'),
    ('Dosa Batter (1 kg)',       'breakfast-cereals',  80,   65, 70, 'Ready to use dosa batter. Crispy dosas every time.'),
    ('Granola (400 g)',          'breakfast-cereals', 250,  219, 50, 'Crunchy honey oat granola. Great with yogurt.'),

    # ── ICE CREAM & DESSERTS (8) ─────────────────────────────────────────────
    ('Vanilla Ice Cream (500 ml)','ice-cream-desserts', 180, 159, 50, 'Classic vanilla ice cream. Smooth and creamy.'),
    ('Chocolate Ice Cream (500 ml)','ice-cream-desserts', 190, 169, 48, 'Rich chocolate ice cream. Chocoholics delight.'),
    ('Strawberry Ice Cream (500 ml)','ice-cream-desserts', 185, None, 45, 'Fresh strawberry ice cream. Fruity and refreshing.'),
    ('Gulab Jamun (500 g)',      'ice-cream-desserts', 120,  99, 55, 'Soft gulab jamuns in sugar syrup. Traditional sweet.'),
    ('Rasgulla (500 g)',         'ice-cream-desserts', 110, None, 60, 'Soft and spongy rasgullas. Bengali delicacy.'),
    ('Halwa Mix (200 g)',        'ice-cream-desserts',  65,   55, 70, 'Instant halwa mix. Ready in minutes.'),
    ('Jelly (100 g)',            'ice-cream-desserts',  30,  None, 90, 'Fruit flavoured jelly. Fun dessert for kids.'),
    ('Custard Powder (100 g)',   'ice-cream-desserts',  55,   45, 75, 'Vanilla custard powder. Great for puddings.'),

    # ── CHOCOLATES & SWEETS (9) ──────────────────────────────────────────────
    ('Dairy Milk (150 g)',       'chocolates-sweets', 150, 129, 90, 'Classic Cadbury milk chocolate. Smooth and creamy.'),
    ('KitKat (4 pack)',          'chocolates-sweets',  80,  None, 100, 'Crispy wafer chocolate. Take a break.'),
    ('5 Star (4 pack)',          'chocolates-sweets',  60,  None, 110, 'Caramel chocolate bar. Energy booster.'),
    ('Ferrero Rocher (16 pcs)', 'chocolates-sweets', 450,  399,  35, 'Premium hazelnut chocolates. Perfect gifting.'),
    ('Oreo Cookies (120 g)',     'chocolates-sweets',  55,   45,  85, 'Classic chocolate sandwich cookies with cream.'),
    ('Dark Chocolate (100 g)',   'chocolates-sweets', 180,  149,  60, '70% dark chocolate. Rich and intense flavor.'),
    ('Milkybar (50 g)',          'chocolates-sweets',  50,  None,  95, 'Creamy white chocolate. Smooth and milky.'),
    ('Kaju Katli (250 g)',       'chocolates-sweets', 350,  319,  30, 'Premium cashew fudge. Festive Indian sweet.'),
    ('Soan Papdi (250 g)',       'chocolates-sweets', 120,   99,  55, 'Flaky cardamom sweet. Classic Indian mithai.'),

    # ── PERSONAL CARE (8) ────────────────────────────────────────────────────
    ('Dove Shampoo (340 ml)',    'personal-care', 280,  249, 60, 'Nourishing shampoo with moisturizing cream. Smooth hair.'),
    ('Dove Soap (100 g)',        'personal-care',  55,  None, 90, 'Moisturizing beauty soap. Gentle on skin.'),
    ('Colgate Toothpaste (200 g)','personal-care', 90,   75, 80, 'Cavity protection toothpaste. Fresh mint flavor.'),
    ('Dettol Handwash (250 ml)', 'personal-care',  95,   79, 75, 'Antibacterial liquid handwash. 99.9% germ protection.'),
    ('Nivea Cream (200 ml)',     'personal-care', 230,  199, 50, 'Moisturizing body cream. Keeps skin soft and smooth.'),
    ('Gillette Shaving Gel',     'personal-care', 200,  179, 45, 'Sensitive skin shaving gel. Smooth and comfortable shave.'),
    ('Sunscreen SPF 50 (50 g)',  'personal-care', 280,  249, 40, 'Broad spectrum sunscreen. Daily UV protection.'),
    ('Sanitizer (500 ml)',       'personal-care',  95,  None, 85, 'Alcohol based hand sanitizer. 99.9% protection.'),

    # ── HOUSEHOLD CLEANING (8) ───────────────────────────────────────────────
    ('Surf Excel (1 kg)',        'household-cleaning', 240, 219, 70, 'Tough stain removing detergent powder.'),
    ('Vim Dishwash Bar',         'household-cleaning',  30,  None, 120, 'Grease cutting dishwash bar. Removes tough stains.'),
    ('Harpic Toilet Cleaner',    'household-cleaning',  95,   79,  75, 'Powerful toilet bowl cleaner. Kills 99.9% germs.'),
    ('Colin Glass Cleaner (500 ml)','household-cleaning', 95, None, 65, 'Streak free glass and surface cleaner.'),
    ('Lizol Floor Cleaner (1 L)','household-cleaning', 145,  129,  60, 'Disinfectant floor cleaner. 10x more germ protection.'),
    ('Garbage Bags (30 pcs)',    'household-cleaning',  55,  None,  90, 'Strong biodegradable garbage bags.'),
    ('Steel Wool (5 pcs)',       'household-cleaning',  40,  None, 100, 'Heavy duty steel wool scrubber. For tough cleaning.'),
    ('Air Freshener (300 ml)',   'household-cleaning', 180,  159,  55, 'Room freshener spray. Long lasting fragrance.'),

    # ── BABY PRODUCTS (7) ────────────────────────────────────────────────────
    ('Cerelac (400 g)',          'baby-products', 360,  329, 40, 'Nestle baby cereal. Enriched with iron and DHA.'),
    ('Pampers Diapers (30 pcs)', 'baby-products', 650,  599, 35, 'Soft and absorbent baby diapers. Keeps baby dry.'),
    ('Johnsons Baby Powder',     'baby-products', 120,  None, 55, 'Gentle talc free baby powder. Keeps skin dry.'),
    ('Johnsons Baby Shampoo',    'baby-products', 150,  129,  50, 'Tear free gentle baby shampoo. No more tears.'),
    ('Farex (500 g)',            'baby-products', 280,  259,  45, 'Weaning cereal for infants. Easy to digest.'),
    ('Baby Wipes (80 pcs)',      'baby-products',  95,   79,  60, 'Soft and moist baby wipes. Gentle on baby skin.'),
    ('Nestum Cereal (300 g)',    'baby-products', 195,  179,  50, 'Multi grain baby cereal. Rich in vitamins.'),

    # ── ORGANIC & NATURAL (8) ────────────────────────────────────────────────
    ('Organic Honey (500 g)',    'organic-natural', 350, 319, 45, '100% pure raw honey. Unprocessed and natural.'),
    ('Organic Turmeric (200 g)','organic-natural', 120,  99, 50, 'Certified organic turmeric powder. High curcumin.'),
    ('Organic Ghee (500 ml)',    'organic-natural', 680, 649, 30, 'A2 milk organic ghee. Bilona method. Pure and natural.'),
    ('Flax Seeds (250 g)',       'organic-natural', 110,  None, 70, 'Organic flax seeds. Rich in omega-3 fatty acids.'),
    ('Chia Seeds (250 g)',       'organic-natural', 180, 159, 55, 'Organic chia seeds. Superfood for energy and health.'),
    ('Moringa Powder (100 g)',   'organic-natural', 250, 219, 40, 'Organic moringa leaf powder. 92 nutrients, 46 antioxidants.'),
    ('Quinoa (500 g)',           'organic-natural', 280, 249, 45, 'Organic white quinoa. Complete protein grain.'),
    ('Apple Cider Vinegar (500 ml)','organic-natural', 280, 249, 50, 'Raw unfiltered ACV with mother. Natural detox.'),

    # ── PET FOOD (7) ─────────────────────────────────────────────────────────
    ('Pedigree Adult (1.4 kg)',  'pet-food', 480, 449, 40, 'Complete adult dog food. Balanced nutrition for dogs.'),
    ('Whiskas Cat Food (1.2 kg)','pet-food', 420, 389, 35, 'Complete cat food. Real fish flavour. Balanced diet.'),
    ('Dog Treats (200 g)',       'pet-food', 180, 159, 50, 'Crunchy dog biscuits. Great for training and reward.'),
    ('Cat Litter (5 kg)',        'pet-food', 350, None, 30, 'Clumping cat litter. Odour control. Easy to clean.'),
    ('Fish Food (100 g)',        'pet-food',  95,  None, 60, 'Flake fish food. Balanced diet for aquarium fish.'),
    ('Dog Shampoo (200 ml)',     'pet-food', 220,  199, 45, 'Gentle dog shampoo. Keeps coat clean and shiny.'),
    ('Pet Dental Chews (10 pcs)','pet-food', 250,  219, 40, 'Dental chews for dogs. Freshens breath, cleans teeth.'),
]


class Command(BaseCommand):
    help = 'Seed database with 22 categories and 200+ products with relevant images'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Delete all existing data before seeding')

    def handle(self, *args, **kwargs):
        if kwargs['reset']:
            self.stdout.write('Deleting existing data...')
            ProductImage.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('Deleted all products and categories.\n'))

        self.stdout.write(self.style.SUCCESS('Seeding categories...\n'))

        cat_map = {}
        for c in CATEGORIES:
            obj, created = Category.objects.get_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'is_active': True}
            )
            cat_map[c['slug']] = obj
            self.stdout.write(f'  {"[Created]" if created else "[Exists] "} {c["name"]}')

        self.stdout.write(self.style.SUCCESS(f'\nSeeding {len(PRODUCTS)} products...\n'))

        tmp_dir = os.path.join(settings.MEDIA_ROOT, 'tmp_seed')
        os.makedirs(tmp_dir, exist_ok=True)

        # Track index per category for image pool cycling
        cat_img_idx = {slug: 0 for slug in IMG}

        created_count = 0
        skipped_count = 0

        for idx, (name, cat_slug, price, sale_price, stock, desc) in enumerate(PRODUCTS):
            if Product.objects.filter(name=name).exists():
                self.stdout.write(f'  [Skip]   {name}')
                skipped_count += 1
                continue

            cat = cat_map[cat_slug]
            product = Product.objects.create(
                category=cat,
                name=name,
                description=desc,
                price=price,
                sale_price=sale_price,
                stock_quantity=stock,
                is_available=True,
            )

            # Get image URL cycling through the pool
            pool = IMG.get(cat_slug, [])
            if pool:
                img_url = pool[cat_img_idx[cat_slug] % len(pool)]
                cat_img_idx[cat_slug] += 1

                img_filename = f'p_{idx+1}.jpg'
                img_path = os.path.join(tmp_dir, img_filename)
                try:
                    req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=15) as response:
                        with open(img_path, 'wb') as f:
                            f.write(response.read())
                    with open(img_path, 'rb') as f:
                        ProductImage.objects.create(
                            product=product,
                            image=File(f, name=img_filename),
                            is_primary=True,
                        )
                    self.stdout.write(f'  [Done]   {name}')
                except Exception as e:
                    self.stdout.write(f'  [NoImg]  {name} ({e})')
            else:
                self.stdout.write(f'  [Done]   {name} (no image pool)')

            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Done! {created_count} products created, {skipped_count} skipped.'
        ))
