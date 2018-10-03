import distribution as dis
import unittest


class TestDistribution(unittest.TestCase):

    # UniformDistribution
    def test_uniform_incorrect_lowest(self):
        test_class = dis.UniformDistribution()
        self.assertRaises(Exception, test_class.set_variables, -1, 2, 3, 4, 5)

    def test_uniform_incorrect_highest(self):
        test_class = dis.UniformDistribution()
        self.assertRaises(Exception, test_class.set_variables, 5, 2, 3, 4, 5)

    def test_uniform_incorrect_highest_2(self):
        test_class = dis.UniformDistribution()
        self.assertRaises(Exception, test_class.set_variables, 1, -2, 3, 4, 5)

    def test_uniform_incorrect_seed(self):
        test_class = dis.UniformDistribution()
        self.assertRaises(Exception, test_class.set_variables, 1, 2, -3, 4, 5)

    def test_uniform_incorrect_multiplication_value(self):
        test_class = dis.UniformDistribution()
        self.assertRaises(Exception, test_class.set_variables, 1, 2, 3, -4, 5)

    def test_uniform_incorrect_add_value(self):
        test_class = dis.UniformDistribution()
        self.assertRaises(Exception, test_class.set_variables, -1, 2, 3, 4, -5)

    def test_uniform_five_constant(self):
        test_class = dis.UniformDistribution()
        test_class.set_variables(5, 5, 3, 4, 5)
        self.assertEqual(test_class.bootstrap(), 5.0)

    def test_uniform_eleven_constant(self):
        test_class = dis.UniformDistribution()
        test_class.set_variables(11, 11)
        self.assertEqual(test_class.bootstrap(), 11.0)

    def test_uniform_five_to_ten(self):
        test_class = dis.UniformDistribution()
        test_class.set_variables(5, 10)
        self.assertTrue(5.0 <= test_class.bootstrap() <= 10.0)

    # ExponentialDistribution
    def test_exponential_incorrect_lowest(self):
        test_class = dis.ExponentialDistribution()
        self.assertRaises(Exception, test_class.set_variables, -1, 2, 3)

    def test_exponential_incorrect_highest(self):
        test_class = dis.ExponentialDistribution()
        self.assertRaises(Exception, test_class.set_variables, 5, 2, 3)

    def test_exponential_incorrect_highest_2(self):
        test_class = dis.ExponentialDistribution()
        self.assertRaises(Exception, test_class.set_variables, 1, -2, 3)

    def test_exponential_incorrect_lambda(self):
        test_class = dis.ExponentialDistribution()
        self.assertRaises(Exception, test_class.set_variables, 1, 2, -3)

    def test_exponential_five_constant(self):
        test_class = dis.ExponentialDistribution()
        test_class.set_variables(5, 5, 3)
        self.assertEqual(test_class.bootstrap(), 5.0)

    def test_exponential_eleven_constant(self):
        test_class = dis.ExponentialDistribution()
        test_class.set_variables(11, 11, 3)
        self.assertEqual(test_class.bootstrap(), 11.0)

    def test_exponential_five_to_ten(self):
        test_class = dis.ExponentialDistribution()
        test_class.set_variables(5, 10, 3)
        self.assertTrue(5.0 <= test_class.bootstrap() <= 10.0)

    # EmpiricalDistribution
    def test_empirical_incorrect_false_type(self):
        test_class = dis.EmpiricalDistribution()
        self.assertRaises(Exception, test_class.set_variables, 123, False)

    def test_empirical_incorrect_interpolation(self):
        test_class = dis.EmpiricalDistribution()
        self.assertRaises(Exception, test_class.set_variables, "empirical_test.txt", "No")

    def test_empirical_incorrect_file_name(self):
        test_class = dis.EmpiricalDistribution()
        self.assertRaises(Exception, test_class.set_variables, "WrongFile.txt", False)

    def test_empirical_five_to_eleven_without_interpolation(self):
        test_class = dis.EmpiricalDistribution()
        test_class.set_variables("empirical_test_five_eleven.txt", False)
        result = test_class.bootstrap()
        self.assertTrue(result == 5.0 or result == 11.0)

    def test_empirical_five(self):
        test_class = dis.EmpiricalDistribution()
        test_class.set_variables("empirical_test.txt", False)
        self.assertTrue(5.0 == test_class.bootstrap())

    def test_empirical_five_to_eleven_with_interpolation(self):
        test_class = dis.EmpiricalDistribution()
        test_class.set_variables("empirical_test_five_eleven.txt", True)
        result = test_class.bootstrap()
        self.assertTrue(5.0 <= result <= 11.0)

    # NoDelayDistribution
    def test_nodelay(self):
        test_class = dis.NoDelayDistribution()
        self.assertEqual(test_class.bootstrap(), 0.0)

    # Probability

    def test_probability_wrong_input(self):
        self.assertRaises(Exception, dis.Probability, 123)

    def test_probability_wrong_input(self):
        test_class = dis.Probability(0)
        self.assertRaises(Exception, dis.Probability.set_chance, 123)

    def test_probability_always_true(self):
        test_class = dis.Probability(1)
        self.assertEqual(test_class.roll(), True)

    def test_probability_always_false(self):
        test_class = dis.Probability(0)
        self.assertEqual(test_class.roll(), False)

if __name__ == '__main__':
    unittest.main()
