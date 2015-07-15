from decider_backend.settings import RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VHOST

broker = 'amqp://' + RABBITMQ_USER + \
         ':'       + RABBITMQ_PASS + \
         '@'       + RABBITMQ_HOST + \
         ':'       + RABBITMQ_PORT + \
         '/'      + RABBITMQ_VHOST

