"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from multiprocessing.connection import wait
from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """

        Thread.__init__(self,**kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time =republish_wait_time
        self.producer_id = marketplace.register_producer()

        pass

    def run(self):
        while True:
            for product in self.products:

                for i in range(product[1]):
                    while True:
                        ret =  self.marketplace.publish(self.producer_id,product[0])
                        if ret == False:
                            sleep(self.republish_wait_time)
                        else:
                            break
                    sleep(product[2])



               
