import datetime

from django.test import TestCase
from django.utils import timezone

from django.core.urlresolvers import reverse

from polls.models import Poll, Choice

class PollMethodsTests (TestCase):

	def test_was_published_recently_with_future_poll(self):
		
		future_poll = Poll(pub_date=timezone.now() +datetime.timedelta(days=30))
		self.assertEqual(future_poll.was_published_recently(), False)
	
	def test_was_published_recently_with_old_poll(self):
		old_poll = Poll(pub_date=timezone.now() - datetime.timedelta (days=30))
		self.assertEqual(old_poll.was_published_recently(),False)

	def test_was_published_recently_with_recent_poll(self):
		recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
		self.assertEqual(recent_poll.was_published_recently(),True)
def create_poll(question, days):
	return Poll.objects.create(question=question,pub_date=timezone.now()+datetime.timedelta(days=days))

def create_choice(poll, choice_text):
	return Choice.objects.create(poll=poll,choice_text=choice_text,votes=0)

class PollViewTests(TestCase):
	def test_index_view_with_no_polls(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_poll_list'],[])

	def test_index_view_with_a_past_poll(self):
		p = create_poll(question="Past poll.",days=-30)
		create_choice(poll=p, choice_text='text')
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'],
			['<Poll: Past poll.>']
		)
	def test_index_view_with_a_future_poll(self):
		p=create_poll(question="Future poll.",days=30)
		response = self.client.get(reverse('polls:index'))
		create_choice(poll=p,choice_text='choice')
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_poll_list'],[])
	
	def test_index_view_with_future_poll_and_past_poll(self):
		p1 = create_poll(question="Future poll.",days=30)
		p2 = create_poll(question="Past poll.",days=-30)
		
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_poll_list'],[])
		
		create_choice(poll=p1,choice_text='past choice')
		create_choice(poll=p2,choice_text='future choice')
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'],
			['<Poll: Past poll.>']
		)
	def test_index_view_with_two_past_polls(self):
		p1 = create_poll(question="Past poll 1.",days=-30)
		p2 = create_poll(question="Past poll 2.",days=-5)
		response = self.client.get(reverse('polls:index'))
		
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_poll_list'],[])
		
		create_choice(poll=p1,choice_text='future choice1')
		create_choice(poll=p2,choice_text='future choice2')
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'],
			['<Poll: Past poll 2.>', '<Poll: Past poll 1.>']
		)

class PollIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_poll(self):
		future_poll = create_poll(question='Future poll.', days=5)
		response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_future_poll_and_a_choice(self):
		future_poll = create_poll(question='Future poll.', days=5)
		create_choice(poll=future_poll,choice_text='choice')
		response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
		self.assertEqual(response.status_code, 404)
	
	def test_detail_view_with_a_past_poll(self):
		past_poll = create_poll(question='Past Poll.', days=-5)
		response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_poll_and_a_choice(self):
		past_poll = create_poll(question='Past Poll.', days=-5)
		create_choice(poll=past_poll,choice_text='choice')
		response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))

class PollRestultsTests(TestCase):
	def test_results_view_with_a_future_poll(self):
		future_poll = create_poll(question='Future poll.', days=5)
		response = self.client.get(reverse('polls:results', args=(future_poll.id,)))
		self.assertEqual(response.status_code, 404)
	
	def test_results_view_with_a_future_poll_choice(self):
		future_poll = create_poll(question='Future poll.', days=5)
		create_choice(poll=future_poll,choice_text='choice')
		response = self.client.get(reverse('polls:results', args=(future_poll.id,)))
		self.assertEqual(response.status_code, 404)

	def test_results_view_with_a_past_poll(self):
		past_poll = create_poll(question='Past Poll.', days=-5)
		
		response = self.client.get(reverse('polls:results', args=(past_poll.id,)))
		self.assertEqual(response.status_code ,404)
	
	def test_results_view_with_a_past_poll_and_a_choice(self):
		past_poll = create_poll(question='Past Poll.', days=-5)
		
		create_choice(poll=past_poll,choice_text='choice')
		response = self.client.get(reverse('polls:results', args=(past_poll.id,)))
		self.assertContains(response, past_poll.question,status_code=200)
