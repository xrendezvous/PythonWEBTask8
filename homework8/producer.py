import pika
import json
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField

fake = Faker()
connect('hw8', host='mongodb+srv://clemontine839:Xzvv9843@cluster0.2lkwevd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')


def generate_fake_contacts(n):
    for _ in range(n):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email()
        ).save()

        message = json.dumps(str(contact.id))
        channel.basic_publish(exchange='',
                              routing_key='email_queue',
                              body=message)
        print(f"Generated and sent to queue: {contact.full_name}")


if __name__ == "__main__":
    generate_fake_contacts(10)