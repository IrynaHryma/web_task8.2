import pika
from faker import Faker

from mongoengine import *
from models import Contact

connect(host ="mongodb+srv://IrynaHryma:2213@cluster7.oesajgi.mongodb.net/web13?retryWrites=true&w=majority",ssl= True)


fake = Faker()
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.queue_declare(queue='email_queue', durable=True)


if __name__=="__main__":
    for _ in range(10):
        full_name= fake.name()
        email = fake.email()
        contact = Contact(full_name = full_name,email = email)

        channel.basic_publish(exchange='',routing_key='email_queue',
        body=str(contact.id).encode())
        
    connection.close()