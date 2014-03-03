//
//  DOUFileManager.h
//  DoubanGroup
//
//  Created by liu yan on 1/27/13.
//  Copyright (c) 2013 Douban. All rights reserved.
//

#import <Foundation/Foundation.h>

#ifndef __DOUFileManager_H__
#define __DOUFileManager_H__

@interface DOUFileManager : NSObject {  
  NSMutableDictionary *_expireDateDictionary;
}

@property (nonatomic, copy, readonly) NSString *baseFilePath;

///--------------------------------------------
/// @name Share Instance Method
///--------------------------------------------
+ (DOUFileManager *)shareCacheFileInstance;
+ (DOUFileManager *)shareTmpFileInstance;
+ (DOUFileManager *)shareOfflineFileInstance;

///--------------------------------------------
/// @name Initial Method
///--------------------------------------------

- (id)initWithBaseFilePath:(NSString *)basePath;

///---------------------------------------------
/// @name Create Parent Directories Method
///---------------------------------------------
- (BOOL)createParentDirectoriesAtPath:(NSString *)path;
- (BOOL)parentDirectoriesExistAtPath:(NSString *)path;

///---------------------------------------------
/// @name Delete Files Method
///---------------------------------------------
- (BOOL)deleteFileAtPath:(NSString *)path;

///---------------------------------------------
/// @name Pares Parent Directory Of The Path Mehtod
///---------------------------------------------
- (NSString *)parseParentDirectoryAtPath:(NSString *)path;

///---------------------------------------------
/// @name Fetch Files Name
///---------------------------------------------
- (NSArray *)fileNamesInParentDirectory:(NSString *)path;

///---------------------------------------------
/// @name Sync Write File Method
///---------------------------------------------

- (BOOL)writeString:(NSString *)string atPath:(NSString *)path;
- (BOOL)writeString:(NSString *)string atPath:(NSString *)path expire:(NSTimeInterval)expire;

- (BOOL)writeData:(NSData *)data atPath:(NSString *)path;
- (BOOL)writeData:(NSData *)data atPath:(NSString *)path expire:(NSTimeInterval)expire;

- (BOOL)writeDictionary:(NSDictionary *)dictionary atPath:(NSString *)path;
- (BOOL)writeDictionary:(NSDictionary *)dictionary atPath:(NSString *)path expire:(NSTimeInterval)expire;

- (BOOL)writeArray:(NSArray *)array atPath:(NSString *)path;
- (BOOL)writeArray:(NSArray *)array atPath:(NSString *)path expire:(NSTimeInterval)expire;

///---------------------------------------------
/// @name Sync Read File Method
///---------------------------------------------
- (NSString *)readStringAtPath:(NSString *)path;

- (NSDictionary *)readDictionaryAtPath:(NSString *)path;

- (NSData *)readDataAtPath:(NSString *)path;

- (NSArray *)readArrayAtPath:(NSString *)path;

///---------------------------------------------
/// @name File Expire Method
///---------------------------------------------
- (void)setExpireTimeInterval:(NSTimeInterval)expireTimeInterval forFilePath:(NSString *)filePath;

- (BOOL)cleanExpireFile;

///-----------------------------------------------
/// @name Vaild File
///-----------------------------------------------
- (BOOL)fileExpiredAtFilePath:(NSString *)filePath;

- (BOOL)fileExistsAtFilePath:(NSString *)filePath;

- (BOOL)fileVaildAtFilePath:(NSString *)filePath;

@end

#endif
