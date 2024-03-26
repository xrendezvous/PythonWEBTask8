from mongoengine import connect, Document, StringField, BooleanField
import pika
import json

connect('hw8', host='mongodb+srv://clemontine839:Xzvv9843@cluster0.2lkwevd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)


def send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Sending email to {contact.full_name} ({contact.email})")
        contact.update(set__message_sent=True)


def callback(ch, method, properties, body):
    contact_id = json.loads(body)
    send_email(contact_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')
channel.basic_consume(queue='email_queue', on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
