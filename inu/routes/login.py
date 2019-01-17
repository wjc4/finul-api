# import logging

from flask import request, jsonify

from inu import application as app
from inu import db
# from inu import sns

# @app.route('/image', methods=['POST'])
# # @app.route('/image/<username>', methods=['POST'])
# def receive_image():
#     # data = request.get_data()
#     # print("rekt")
#     # print(data)
#     username='anonymous'
#     result = db.get(db_entry)
#     status = result[username]['status']
#     if status == 3:
#         return jsonify({'status': result[username]['status']})
    
#     names = list(request.files.keys())
#     username = names[0]
#     try:
#         personId = result[username]['personId']
#     except:
#         personId = 'a97bf5e8-1e67-4970-a37a-a3be941fee96'

#     valid = False
#     for name in names:
#         # first receive the file from the raspi
#         print('received')
#         fileImg = request.files[name].read()
#         # filename = request.files[name].filename
#         print(type(fileImg))
#         # print(fileImg)
#         im = Image.open(io.BytesIO(fileImg))
        
#         try:
#             im.verify()
#             print('Valid image')
#             if im.format == 'JPEG':
#                 # imgByteArr = io.BytesIO()
#                 # roiImg.save(imgByteArr, format='JPEG')
#                 # fileImg = imgByteArr.getvalue()
#                 valid = True
#                 print('JPEG image')
#                 break
#             else:
#                 print('Invalid image type')
#         except Exception:
#             print('Invalid image')
#         if valid:
#             break
#         # nameSaved = './static/' + str(time.time()).replace('.', '')[-3:] + filename
#         # im.save(nameSaved)

#     # im = Image.open(io.BytesIO(fileImg))
#     # im = im.rotate(90)
#     # imgByteArr = io.BytesIO()
#     # im.save(imgByteArr, format='JPEG')
#     # fileImg = imgByteArr.getvalue()

#     global reference_image
#     if status == 0:
#         print('recognising')
#         correct, face_attributes = check_image(
#             fileImg, personId, personGroupId)
#         if correct:
#             result[username]['status'] = 1
#             db.update(db_entry, result)
#             result[username]['emotions'] = face_attributes
#             reference_image = fileImg
#     elif status == 1:
#         # do liveliness check 1
#         ref_im = Image.open(io.BytesIO(reference_image))
#         ref_im = ref_im.rotate(270)
#         ref_lm = np.asarray(pe.get_features(ref_im))
#         im = Image.open(io.BytesIO(fileImg))
#         im = im.rotate(270)
#         lm = np.asarray(pe.get_features(im))
#         if lm is None:
#             return jsonify({'status': 1})
#         verify = pe.check_mouth_open(ref_lm, lm)
#         if verify:
#             print("Mouth open")
#             result[username]['status'] = 2
#             db.update(db_entry, result)
#     elif status == 2:
#         # do liveliness check 2
#         ref_im = Image.open(io.BytesIO(reference_image))
#         ref_im = ref_im.rotate(270)
#         ref_lm = np.asarray(pe.get_features(ref_im))
#         im = Image.open(io.BytesIO(fileImg))
#         im = im.rotate(270)
#         lm = np.asarray(pe.get_features(im))
#         if lm is None:
#             return jsonify({'status': 2})
#         verify = pe.tilt_head_check(ref_lm, lm)
#         if verify:
#             print("Head tilted")
#             result[username]['status'] = 3
#             db.update(db_entry, result)
#     return jsonify({'status': result[username]['status']})

# @app.route('/login', methods=['GET'])
# # @app.route('/login/<username>', methods=['GET'])
# def login(username='anonymous'):
#     result = db.get(db_entry)
#     if username not in result:
#         result[username] = {}
#     result[username]['status'] = 0
#     db.update(db_entry, result)
#     number = random.randint(111111,999999)
#     sns.insert(number)
#     return jsonify({'status': result[username]['status']})

# @app.route('/register', methods=['POST'])
# # @app.route('/register/<username>', methods=['POST'])
# def register(username='anonymous'):
#     names = list(request.files.keys())
#     for name in names:
#         # first receive the file from the raspi
#         print('received')
#         fileImg = request.files[name].read()
#         # filename = request.files[name].filename
#         print(type(fileImg))
#         # print(fileImg)
#         im = Image.open(io.BytesIO(fileImg))
        
#         try:
#             im.verify()
#             print('Valid image')
#             if im.format == 'JPEG':
#                 print('JPEG image')
#                 break
#             else:
#                 print('Invalid image type')
#         except Exception:
#             print('Invalid image')
#         if valid:
#             break

#     im = im.rotate(270)
#     image_bytes = io.BytesIO()
#     im.save(image_bytes, format='JPEG')
#     image_bytes = image_bytes.getvalue()
#     # image_bytes = fileImg

#     personId = create_person(username)
#     add_face(image_bytes, personId, personGroupId)
#     result = db.get(db_entry)
#     result[username]['personId'] = personId
#     db.update(db_entry, result)

# @app.route('/status', methods=['GET'])
# # @app.route('/status/<username>', methods=['GET'])
# def status(username='anonymous'):
#     result = db.get(db_entry)
#     return jsonify({'status': result[username]['status']})

# @app.route('/emotions', methods=['GET'])
# # @app.route('/emotions/<username>', methods=['GET'])
# def emotions(username='anonymous'):
#     result = db.get(db_entry)
#     return jsonify({'emotions': result[username]['emotions']})