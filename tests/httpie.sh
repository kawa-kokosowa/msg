#!/bin/sh

# Populate the database with some dummy data.
http POST http://localhost:5000/user username=cutie password=woop
http POST http://localhost:5000/user username=witch password=zap
http POST http://localhost:5000/user username=ghost password=boo
http POST http://localhost:5000/user username=pumpkin password=lantern

http POST http://localhost:5000/message text="First post by cutie." --auth cutie:woop
http POST http://localhost:5000/message text="Second post by witch." --auth witch:zap
http POST http://localhost:5000/message text="Third post by ghost." --auth ghost:boo
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern
http POST http://localhost:5000/message text="Middle post by pumpkin." --auth pumpkin:lantern

http POST http://localhost:5000/message text="Third to last post by ghost." --auth ghost:boo
http POST http://localhost:5000/message text="Second to last post by witch." --auth witch:zap
http POST http://localhost:5000/message text="Last post by cutie." --auth cutie:woop
