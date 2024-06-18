def generate_cnn_model_vgg16():

    vgg_conv = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
    
    model = Sequential()

    for layer in vgg_conv.layers[:-5]:
        layer.trainable = False

    for layer in vgg_conv.layers:
        print(layer, layer.trainable)

    model.add(vgg_conv)
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(2, activation='softmax'))

    model.summary()
    
    opt = Adam(learning_rate=1e-3, epsilon=0.1)
    model.compile(loss='binary_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    
    return model
