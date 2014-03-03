//
//  DOUFileManager+Asynchronous.h
//  DoubanGroup
//
//  Created by liu yan on 1/28/13.
//  Copyright (c) 2013 Douban. All rights reserved.
//

#ifndef __DOUFileManager_Asyn_H__
#define __DOUFileManager_Asyn_H__

#import "DOUFileManager.h"

typedef void(^complete)(BOOL success);

@interface DOUFileManager (Asynchronous)

///---------------------------------------------
/// @name Async Write File Method
///---------------------------------------------
- (void) asyncWriteData:(NSData *)data atPath:(NSString *)path complete:(complete)complete;

- (void) asyncWriteDictionary:(NSDictionary *)dictionary atPath:(NSString *)path complete:(complete)complete;

- (void) asyncWriteString:(NSString *)string atPath:(NSString *)path complete:(complete)complete;

- (void) asyncWriteArray:(NSArray *)array atPath:(NSString *)path complete:(complete)complete;

- (void) asyncWriteData:(NSData *)data atPath:(NSString *)path expire:(NSTimeInterval)expire complete:(complete)complete;

- (void) asyncWriteDictionary:(NSDictionary *)dictionary atPath:(NSString *)path expire:(NSTimeInterval)expire complete:(complete)complete;

- (void) asyncWriteString:(NSString *)string atPath:(NSString *)path expire:(NSTimeInterval)expire complete:(complete)complete;

- (void) asyncWriteArray:(NSArray *)array atPath:(NSString *)path expire:(NSTimeInterval)expire complete:(complete)complete;

///---------------------------------------------
/// @name Async Read File Method
///---------------------------------------------
- (void) asyncReadStringAtPath:(NSString *)path complete:(void(^)(NSString *resultString))complete;

- (void) asyncReadDataAtPath:(NSString *)path complete:(void(^)(NSData *resultData))complete;

- (void) asyncReadDictionaryAtPath:(NSString *)path complete:(void(^)(NSDictionary *resultDictionary))complete;

- (void) asyncReadArrayAtPath:(NSString *)path complete:(void(^)(NSArray *resultArray))complete;

///---------------------------------------------
/// @name Async Delete File Method
///---------------------------------------------
- (void) asyncDeleteFileAtPath:(NSString *)path complete:(complete)complete;

- (void) asyncCleanExpireFile:(complete)complete;

@end

#endif
