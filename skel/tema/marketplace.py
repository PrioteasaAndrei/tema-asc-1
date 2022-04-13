"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""


from asyncio.log import logger
from distutils.log import INFO
from multiprocessing import Lock, Semaphore
import unittest
import logging
from logging.handlers import RotatingFileHandler

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    ## this will skip some indeces but assures that each id is unique
    producer_id = -1
    cart_id = -1 

    ## -77 means the product is not reserved


    ## logging 

   ## my_logger = logging.basicConfig(filename='marketplace_logger',level=logging.INFO)




    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """

        logger = logging.getLogger("marketplace_logger")
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler("marketplace.log",maxBytes=5000000,backupCount=5)
        logger.addHandler(handler)

        self.logger = logger

        buf = "__init__ : queue_size_per_producer: {}".format(queue_size_per_producer)
        logger.info(buf)
        self.queue_size_per_producer =queue_size_per_producer
 
        self.products_queue = {}
        self.consumer_baskets = {}

        self.my_lock = Lock()
        self.lock_add_cart = Lock()
        self.lock_publish = Lock()
        

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        buf = "register_producer: {}".format(Marketplace.producer_id + 1)
        self.logger.info(buf)

        with self.my_lock:

            Marketplace.producer_id += 1
            aux = 'producer-' + str(Marketplace.producer_id)
            self.products_queue[aux] = []
            return aux


    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        buf = 'publish: producer_id {} product {}'.format(producer_id,product)
        self.logger.info(buf)

        publish_worked = False
        with self.lock_publish:

            if producer_id in self.products_queue:
                if len(self.products_queue[producer_id]) < self.queue_size_per_producer:
                    ## -77 pt ca nu e rezervat de cineva
                    self.products_queue[producer_id].append((product,-77))
                    buf = '\tappended {} with -77 as unclaimed object'.format(product)
                    self.logger.info(buf)
                    publish_worked = True
                    
        
        return publish_worked


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        
        buf = 'new_cart: {}'.format(Marketplace.cart_id + 1)
        self.logger.info(buf)



        Marketplace.cart_id += 1
        self.consumer_baskets[self.cart_id] = [] 
        return Marketplace.cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        buf = 'add_to_cart: cart_id {} product {}'.format(cart_id,product)
        self.logger.info(buf)

        found_product_key = None
        cart_id_found = False 
        with self.lock_add_cart:


            if cart_id in self.consumer_baskets:
                cart_id_found = True
                for key in self.products_queue:
                    for prod,reserved in self.products_queue[key]:
                        if prod == product and reserved == -77:
                            ## == overriten in class product
                            found_product_key = key 
                            buf = 'Found a product to reserve'
                            self.logger.info('\t' + buf)
                            break

                if found_product_key != None:
                    ## reserve it 
                    index = self.products_queue[found_product_key].index((product,-77))
                    buf = '\tReserving {} with cart_id {} index is: {}'.format(product,cart_id,index)
                    self.logger.info(buf)
                    self.products_queue[found_product_key][index] = (product,cart_id)
                    ## put tuples of product and key of producer so i can remove it later and put it
                    ## in the right list 
                    self.consumer_baskets[cart_id].append((product,found_product_key))
                    buf = '\tAppended {} of producer {} to cart_id {}'.format(product,found_product_key,cart_id)
                    self.logger.info(buf)

        
        if cart_id_found and found_product_key != None:
            return True
        

        buf = '\tNo product found to reserve'
        self.logger.info(buf)

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        buf = 'remove_from_cart: cart_id {} product {}'.format(cart_id,product)
        self.logger.info(buf)

        for basket_product,original_producer_id in self.consumer_baskets[cart_id]:
            if basket_product == product:
                self.consumer_baskets[cart_id].remove((product,original_producer_id))
                buf = '\tRemoved {} of {} from {}'.format(product,original_producer_id,cart_id)
                self.logger.info(buf)
                index = self.products_queue[original_producer_id].index((product,cart_id))
                self.products_queue[original_producer_id][index] = (product,-77)
                buf = 'Unclaimed product {} of {}'.format(product,original_producer_id)
                self.logger.info(buf)
                break


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """

        buf = 'place_order: cart_id {}'.format(cart_id)
        self.logger.info(buf)

        ret = [] 

        for product,original_producer_id in self.consumer_baskets[cart_id]:

            self.products_queue[original_producer_id].remove((product,cart_id))
            buf = '\tRemoved {} from {} queue because an order is placed'.format(product,original_producer_id)
            self.logger.info(buf)
            ret.append(product)
            buf = "cons%d bought %s\n" % (cart_id+1,product)
            print(buf)
            
        self.consumer_baskets[cart_id] = [] 

        return ret 



class TestMarketplace(unittest.TestCase):
    
    def setUp(self,queue_size_per_producer):
        self.marketplace = Marketplace(queue_size_per_producer)

    def test_register_producer(self):
        pass

    def test_publish(self, producer_id, product):
        pass

    def test_new_cart(self):
        pass

    def test_add_to_cart(self, cart_id, product):
        pass

    def test_remove_from_cart(self, cart_id, product):
        pass

    def test_place_order(self, cart_id):
        pass
