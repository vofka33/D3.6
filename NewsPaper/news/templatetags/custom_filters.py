from django import template


register = template.Library()



@register.filter()
def censor(text):
   if type(text) != str:
      return ('приходит неверный тип данных')

   bad_words = ['редиска', 'вжик']
   filtred_message = ''

   for word in text.split():
      word2 = word.strip(' ., !() ').lower()
      if word2 in bad_words:
         word2 = word[:1] + ('*' * (len(word2) - 1))

         if len(word2) < len(word):
            word2 += word[-1]
         filtred_message += f'{word2} '

      else:
         filtred_message += f'{word} '
   return filtred_message
