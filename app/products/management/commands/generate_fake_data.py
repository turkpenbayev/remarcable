from django.core.management.base import BaseCommand
from faker import Faker
from products.models import Category, Tag, Product
import random

class Command(BaseCommand):
    help = 'Generate fake data for products'

    def handle(self, *args, **kwargs):
        fake = Faker()

        total = 50
        
        # Create categories
        categories = [Category.objects.create(name=fake.word()) for _ in range(5)]

        # Create tags
        tags = [Tag.objects.create(name=fake.word()) for _ in range(10)]

        # Create products
        for _ in range(total):
            name = fake.name()
            category = random.choice(categories)
            product = Product.objects.create(name=name, category=category)
            
            # Assign random tags to products
            random_tags = random.sample(tags, random.randint(1, 3))
            product.tags.set(random_tags)
            
            self.stdout.write(self.style.SUCCESS(f"Created product: {name}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {total} fake products"))
