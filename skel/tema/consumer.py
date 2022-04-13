"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self,**kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.cart_id = self.marketplace.new_cart()

    def run(self):
        for cart in self.carts:
           ## print("CART",cart)
            for op in cart:
                ##print('OP',op)
                if op['type'] == 'add':
                    for i in range(op["quantity"]):
                        while True:
                            ret =  self.marketplace.add_to_cart(self.cart_id,op['product'])
                            if ret == True:
                               # print('Consumer added to cart: ',op['product'])
                                break
                            else:
                               # print('Consumer didnt find the product - wait')
                                sleep(self.retry_wait_time)
                            
                elif op['type'] == 'remove':
                    #print('Consumer removed from cart: ',op['product'])
                    
                    for i in range(op["quantity"]):
                        self.marketplace.remove_from_cart(self.cart_id,op['product'])


            self.marketplace.place_order(self.cart_id)
        
                   
