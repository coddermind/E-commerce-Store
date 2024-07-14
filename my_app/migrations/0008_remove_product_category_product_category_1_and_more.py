# Generated by Django 5.0.6 on 2024-06-10 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0007_alter_product_category_alter_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category_1',
            field=models.CharField(choices=[('all', 'All'), ('mobile_phones_accessories', 'Mobile Phones & Accessories'), ('computers_accessories', 'Computers & Accessories'), ('cameras_photography', 'Cameras & Photography'), ('audio_home_theater', 'Audio & Home Theater'), ('wearable_technology', 'Wearable Technology'), ('gaming', 'Gaming'), ('home_appliances', 'Home Appliances'), ('smart_home_devices', 'Smart Home Devices'), ('jewelry', 'Jewelry'), ('bags_wallets', 'Bags & Wallets'), ('watches', 'Watches'), ('hats_caps', 'Hats & Caps'), ('sunglasses_eyewear', 'Sunglasses & Eyewear'), ('belts', 'Belts'), ('scarves_shawls', 'Scarves & Shawls'), ('footwear_accessories', 'Footwear Accessories'), ('hair_accessories', 'Hair Accessories'), ('gloves_mittens', 'Gloves & Mittens'), ('women_unstitch', 'Women Unstitch'), ('sports_equipment', 'Sports Equipment'), ('outdoor_gear', 'Outdoor Gear'), ('health_beauty', 'Health & Beauty'), ('toys_games', 'Toys & Games'), ('baby_products', 'Baby Products'), ('office_supplies', 'Office Supplies'), ('musical_instruments', 'Musical Instruments'), ('books', 'Books'), ('furniture', 'Furniture'), ('pet_supplies', 'Pet Supplies')], default='all', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='category_2',
            field=models.CharField(blank=True, choices=[('all', 'All'), ('mobile_phones_accessories', 'Mobile Phones & Accessories'), ('computers_accessories', 'Computers & Accessories'), ('cameras_photography', 'Cameras & Photography'), ('audio_home_theater', 'Audio & Home Theater'), ('wearable_technology', 'Wearable Technology'), ('gaming', 'Gaming'), ('home_appliances', 'Home Appliances'), ('smart_home_devices', 'Smart Home Devices'), ('jewelry', 'Jewelry'), ('bags_wallets', 'Bags & Wallets'), ('watches', 'Watches'), ('hats_caps', 'Hats & Caps'), ('sunglasses_eyewear', 'Sunglasses & Eyewear'), ('belts', 'Belts'), ('scarves_shawls', 'Scarves & Shawls'), ('footwear_accessories', 'Footwear Accessories'), ('hair_accessories', 'Hair Accessories'), ('gloves_mittens', 'Gloves & Mittens'), ('women_unstitch', 'Women Unstitch'), ('sports_equipment', 'Sports Equipment'), ('outdoor_gear', 'Outdoor Gear'), ('health_beauty', 'Health & Beauty'), ('toys_games', 'Toys & Games'), ('baby_products', 'Baby Products'), ('office_supplies', 'Office Supplies'), ('musical_instruments', 'Musical Instruments'), ('books', 'Books'), ('furniture', 'Furniture'), ('pet_supplies', 'Pet Supplies')], max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='category_3',
            field=models.CharField(blank=True, choices=[('all', 'All'), ('mobile_phones_accessories', 'Mobile Phones & Accessories'), ('computers_accessories', 'Computers & Accessories'), ('cameras_photography', 'Cameras & Photography'), ('audio_home_theater', 'Audio & Home Theater'), ('wearable_technology', 'Wearable Technology'), ('gaming', 'Gaming'), ('home_appliances', 'Home Appliances'), ('smart_home_devices', 'Smart Home Devices'), ('jewelry', 'Jewelry'), ('bags_wallets', 'Bags & Wallets'), ('watches', 'Watches'), ('hats_caps', 'Hats & Caps'), ('sunglasses_eyewear', 'Sunglasses & Eyewear'), ('belts', 'Belts'), ('scarves_shawls', 'Scarves & Shawls'), ('footwear_accessories', 'Footwear Accessories'), ('hair_accessories', 'Hair Accessories'), ('gloves_mittens', 'Gloves & Mittens'), ('women_unstitch', 'Women Unstitch'), ('sports_equipment', 'Sports Equipment'), ('outdoor_gear', 'Outdoor Gear'), ('health_beauty', 'Health & Beauty'), ('toys_games', 'Toys & Games'), ('baby_products', 'Baby Products'), ('office_supplies', 'Office Supplies'), ('musical_instruments', 'Musical Instruments'), ('books', 'Books'), ('furniture', 'Furniture'), ('pet_supplies', 'Pet Supplies')], max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='category_4',
            field=models.CharField(blank=True, choices=[('all', 'All'), ('mobile_phones_accessories', 'Mobile Phones & Accessories'), ('computers_accessories', 'Computers & Accessories'), ('cameras_photography', 'Cameras & Photography'), ('audio_home_theater', 'Audio & Home Theater'), ('wearable_technology', 'Wearable Technology'), ('gaming', 'Gaming'), ('home_appliances', 'Home Appliances'), ('smart_home_devices', 'Smart Home Devices'), ('jewelry', 'Jewelry'), ('bags_wallets', 'Bags & Wallets'), ('watches', 'Watches'), ('hats_caps', 'Hats & Caps'), ('sunglasses_eyewear', 'Sunglasses & Eyewear'), ('belts', 'Belts'), ('scarves_shawls', 'Scarves & Shawls'), ('footwear_accessories', 'Footwear Accessories'), ('hair_accessories', 'Hair Accessories'), ('gloves_mittens', 'Gloves & Mittens'), ('women_unstitch', 'Women Unstitch'), ('sports_equipment', 'Sports Equipment'), ('outdoor_gear', 'Outdoor Gear'), ('health_beauty', 'Health & Beauty'), ('toys_games', 'Toys & Games'), ('baby_products', 'Baby Products'), ('office_supplies', 'Office Supplies'), ('musical_instruments', 'Musical Instruments'), ('books', 'Books'), ('furniture', 'Furniture'), ('pet_supplies', 'Pet Supplies')], max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='category_5',
            field=models.CharField(blank=True, choices=[('all', 'All'), ('mobile_phones_accessories', 'Mobile Phones & Accessories'), ('computers_accessories', 'Computers & Accessories'), ('cameras_photography', 'Cameras & Photography'), ('audio_home_theater', 'Audio & Home Theater'), ('wearable_technology', 'Wearable Technology'), ('gaming', 'Gaming'), ('home_appliances', 'Home Appliances'), ('smart_home_devices', 'Smart Home Devices'), ('jewelry', 'Jewelry'), ('bags_wallets', 'Bags & Wallets'), ('watches', 'Watches'), ('hats_caps', 'Hats & Caps'), ('sunglasses_eyewear', 'Sunglasses & Eyewear'), ('belts', 'Belts'), ('scarves_shawls', 'Scarves & Shawls'), ('footwear_accessories', 'Footwear Accessories'), ('hair_accessories', 'Hair Accessories'), ('gloves_mittens', 'Gloves & Mittens'), ('women_unstitch', 'Women Unstitch'), ('sports_equipment', 'Sports Equipment'), ('outdoor_gear', 'Outdoor Gear'), ('health_beauty', 'Health & Beauty'), ('toys_games', 'Toys & Games'), ('baby_products', 'Baby Products'), ('office_supplies', 'Office Supplies'), ('musical_instruments', 'Musical Instruments'), ('books', 'Books'), ('furniture', 'Furniture'), ('pet_supplies', 'Pet Supplies')], max_length=100),
        ),
    ]
