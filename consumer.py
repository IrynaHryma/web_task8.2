import pika

from mongoengine import *

from models import Contact

connect(host ="mongodb+srv://IrynaHryma:2213@cluster7.oesajgi.mongodb.net/web13?retryWrites=true&w=majority",ssl= True)


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.queue_declare(queue='email_queue',durable=True)

def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects.get(id=contact_id)
    contact.message_sent = True
    contact.save()


channel.basic_consume(queue='email_queue', on_message_callback=callback,auto_ack=True)


if __name__ == '__main__':
    channel.start_consuming()