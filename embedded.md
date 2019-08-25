### Use manga-py in your project


```python
from manga_py.parser import Parser
from manga_py.info import Info


my_awesome_handler = open('my-handler')


class MyAwesomeInfo(Info):
    pass


# main class (you will have your own)
class MyAwesomeClass:
    args = {}
    """
    is just a Namespace or dict with arguments
     (filled below. You can implement your implementation. The main thing is to have all keys possible)
    see manga_py.cli.args.get_cli_arguments()
    """

    parser = None  # the found parser gets here (see below)

    def get_info(self):
        MyAwesomeInfo(self.args)  # use the Info class from manga-py or overload the Info class from manga-py

    def start(self):
        self.parser = Parser(self.args)
        try:
            self.parser.init_provider(
                progress=self.progress,
                log=self.print,
                quest=self.quest,
                quest_password=self.quest_password,
                info=self.get_info(),
            )
        except AttributeError as e:
            raise e
        self.parser.start()  # provider main method

    def progress(self, items_count: int, current_item: int, re_init: bool = False): # the same progress function. re_init = True means "next chapter"
        # simple progress
        pass

    def print(self, text, **kwargs):
        """
        Not used everywhere. Better reload global print method
        """
        print(text, **kwargs, file=my_awesome_handler)

    def quest(self, variants: enumerate, title: str, select_type=0):  # 0 = single, 1 = multiple
        if select_type == 0:
            print(' Question ')
            return 'Answer'
        else:
            print(' Question multiple answers')
            return [
                'Answer 1',
                'Answer 2',
                ...
            ]

    def quest_password(self, title):
        """
        used to ask user password
        """
        print(title)
        return 'my_awesome_password'
```
