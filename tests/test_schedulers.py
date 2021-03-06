from django.test import TestCase
from css.models import *

class schedulerTestCase(TestCase):
    # Utility Functions 
    @staticmethod
    def create_scheduler(email='email@email.com', password='password#0',
                       user_type='scheduler', first_name='blah', last_name='blah'):
        return CUser.create(email, password, user_type, first_name, last_name)

    @staticmethod
    def get_scheduler(email=None):
        return CUser.get_scheduler(email=email)

    @staticmethod
    def get_all_schedulers():
        return CUser.objects.filter(user_type='scheduler')

    def verify_scheduler(self, scheduler, email='email@email.com', password='password#0',
                         first_name='blah', last_name='blah'):
        self.assertTrue(isinstance(scheduler, CUser))
        self.assertEqual(scheduler.user.username, email)
        self.assertEqual(scheduler.user.email, email)
        self.assertTrue(scheduler.user.check_password(password))
        self.assertEqual(scheduler.user_type, 'scheduler')
        self.assertEqual(scheduler.user.first_name, first_name)
        self.assertEqual(scheduler.user.last_name, last_name)

    # begin tests
    def test_valid_scheduler(self):     
        scheduler = self.create_scheduler()
        self.verify_scheduler(scheduler, 'email@email.com', 'password#0', 'blah', 'blah')
        scheduler.delete()
        self.assertRaises(ObjectDoesNotExist, self.get_scheduler, email='email@email.com')

    def test_valid_scheduler(self):     
        scheduler1 = self.create_scheduler(email='email1@email.com')
        scheduler2 = self.create_scheduler(email='email2@email.com')
        self.verify_scheduler(scheduler1, email='email1@email.com')
        self.verify_scheduler(scheduler2, email='email2@email.com')
        self.assertTrue(scheduler1 in self.get_all_schedulers())
        self.assertTrue(scheduler2 in self.get_all_schedulers())
        scheduler1.delete()
        scheduler2.delete()
        self.assertRaises(ObjectDoesNotExist, self.get_scheduler, email='email@email1.com')
        self.assertRaises(ObjectDoesNotExist, self.get_scheduler, email='email@email2.com')

    # Email
    def test_valid_email_1(self):
        scheduler = self.create_scheduler(email='vito.dinovi@gmail.com')
        self.verify_scheduler(scheduler, email='vito.dinovi@gmail.com')
        scheduler.delete()
        self.assertRaises(ObjectDoesNotExist, self.get_scheduler, email='vito.dinovi@gmail.com')

    def test_valid_email_2(self):
        scheduler = self.create_scheduler(email='vdinovi@calpoly.edu')
        self.verify_scheduler(scheduler, email='vdinovi@calpoly.edu')
        scheduler.delete()
        self.assertRaises(ObjectDoesNotExist, self.get_scheduler, email='vdinovi@calpoly.edu')

    def test_invalid_email_1(self):
        self.assertRaises(ValidationError, self.create_scheduler, email='')

    def test_invalid_email_2(self):     
        self.assertRaises(ValidationError, self.create_scheduler, email='email')

    def test_invalid_email_3(self):     
        self.assertRaises(ValidationError, self.create_scheduler, email='@test.com')

    # Password
    def test_valid_password_1(self):
        scheduler = self.create_scheduler(password='1.aaAZaa')
        self.assertTrue(scheduler.user.check_password('1.aaAZaa'))
        scheduler.delete()

    def test_valid_password_2(self):
        scheduler = self.create_scheduler(password='u*1zz+F?T')
        self.assertTrue(scheduler.user.check_password('u*1zz+F?T'))
        scheduler.delete()

    def test_invalid_password_1(self):     
        self.assertRaises(ValidationError, self.create_scheduler, password='')

    def test_invalid_password_2(self):
        self.assertRaises(ValidationError, self.create_scheduler, password='aaaaaaaaaaaaaaaaaaaaaaaaaaaaa$1aa')

    def test_invalid_password_3(self):
        self.assertRaises(ValidationError, self.create_scheduler, password='1$aaaaa')

    def test_invalid_password_4(self):
        self.assertRaises(ValidationError, self.create_scheduler, password='1234567!')

    # User type
    def test_invalid_user_type(self):
        self.assertRaises(ValidationError, self.create_scheduler, user_type='aaa')

    # Filter
    def test_filter_scheduler_1(self):
        scheduler1 = self.create_scheduler(email='scheduler1@email.com',
                                  user_type='scheduler')
        scheduler2 = self.create_scheduler(email='scheduler2@email.com',
                                           user_type='faculty')
        scheduler_list = self.get_all_schedulers()
        self.assertTrue(scheduler1 in scheduler_list)
        self.assertTrue(scheduler2 not in scheduler_list)
        scheduler1.delete()
        scheduler2.delete()

    def test_filter_scheduler_2(self):
        scheduler1 = self.create_scheduler(email='scheduler1@email.com',
                                  user_type='faculty')
        scheduler2 = self.create_scheduler(email='scheduler2@email.com',
                                  user_type='faculty')
        self.assertTrue(not self.get_all_schedulers()) 
        scheduler1.delete()
        scheduler2.delete()

    # DoesNotExist
    def test_invalid_get_scheduler(self):
        self.assertRaises(ObjectDoesNotExist, self.get_scheduler, email='aaaaaaaaa')

    def test_invalid_get_scheduler(self):
        self.create_scheduler()
        self.assertRaises(ObjectDoesNotExist, self.get_scheduler, email='aaaaaaaaa')

    # Duplicate
    def test_duplicate_scheduler(self):
        scheduler1 = self.create_scheduler()
        self.assertRaises(IntegrityError, self.create_scheduler)

    # Delete
    def test_delete_scheduler(self):
        scheduler = self.create_scheduler(email='email@email.com')
        self.assertTrue(scheduler in self.get_all_schedulers())
        scheduler.delete()
        self.assertTrue(scheduler not in self.get_all_schedulers())
        self.assertRaises(ObjectDoesNotExist, self.get_scheduler, email='email@email.com')

