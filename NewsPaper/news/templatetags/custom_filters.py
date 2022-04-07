from django import template


register = template.Library()



@register.filter()
def censor(text):
   if type(text) != str:
      return ('приходит неверный тип данных')

   bad_words = ['редиска', 'вжик']
   filtred_message = ''
   string = ''
      
   for i in text:
      string += i
      string2 = string.lower()

      flag = 0
      for j in bad_words:
         if not string2 in j:
            flag += 1
         if string2 == j:
            filtred_message += string[:1] + '*' * (len(string) - 1)
            flag -= 1
            string = ''

      if flag == len(bad_words):
         filtred_message += string
         string = ''

   if string2 != '' and string2 not in bad_words:
      filtred_message += string
   elif string2 != '':
      filtred_message += string + '*' * len(string)
   return filtred_message