# coding: utf8

from datetime import datetime

db.define_table('diet_item',
    Field('owner_id', 'reference auth_user', default=auth.user_id, writable=False, readable=False,
        requires=IS_IN_DB(db, 'auth_user.id', 'auth_user.email')),
    Field('name', requires=IS_NOT_EMPTY()),
    Field('type'),
    Field('brand'),
    Field('description', 'text'),
    Field('serving_size'),
    Field('calories'),
    Field('calories_from_fat'),
    Field('total_fat_g'),
    Field('saturated_fat_g'),
    Field('trans_fat_g'),
    Field('cholesterol_mg'),
    Field('sodium_mg'),
    Field('carbohydrates_g'),
    Field('dietary_fiber_g'),
    Field('sugars_g'),
    Field('protein_g')
)

db.define_table('meal',
    Field('owner_id', 'reference auth_user', default=auth.user_id, writable=False, readable=False,
        requires=IS_IN_DB(db, 'auth_user.id', 'auth_user.email')),
    Field('name', requires=IS_NOT_EMPTY()),
    Field('dt', 'datetime', default=request.now, requires=IS_NOT_EMPTY())
)

"""
    add stats to meal like calories, carbs, protein. allow preferences to be set.
    update every time a meal_item is added or 
"""

db.define_table('meal_items',
    Field('meal_id', 'reference meal', requires=IS_IN_DB(db, 'meal.id', 'meal.name', 'meal.dt')),
    Field('num_servings', requires=IS_NOT_EMPTY()),
    Field('diet_item_id', 'reference diet_item',
        requires=IS_IN_DB(db, 'diet_item.id', 'diet_item.name', 'diet_item.serving_size'))
)


"""
    'exercise_set'
    'workout'
    'workout_items'
"""
