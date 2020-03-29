import motor.motor_asyncio
import logging
import os



class mongo_db:

    def __init__(self, logger: logging.Logger=None):
        self.logger = logger if logger is not None else logging.getLogger("mongo_db class")

        client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
        self.db = client['bot']

    async def get_questions(self):
        self.collection = self.db['questions']

        document = {'key': 'value'}
        result = await self.collection.insert_one(document)
        print('result %s' % repr(result.inserted_id))

        print(self.collection)

    async def insert_question(self, question_text, question_author_id):
        collection = self.db['questions']

        document = {
            'question_text': question_text,
            'question_author_id': question_author_id,
            'answers': [],
        }
        print(document)
        result = await collection.insert_one(document)
        return result.inserted_id

    async def insert_answer(self, question_id, answer_text):
        collection = self.db['questions']
        find = await collection.find_one({'_id': question_id})
        document = dict(find)
        document['answers'].append({'answer_text': answer_text})
        await collection.update_one({'_id': question_id}, {'$set': document})

    async def insert_number_ball(self, question_id, answer_text):
        collection = self.db['questions']
        find = await collection.find_one({'_id': question_id})
        document = dict(find)
        document['answers'].append({'answer_text': answer_text})
        await collection.update_one({'_id': question_id}, {'$set': document})
