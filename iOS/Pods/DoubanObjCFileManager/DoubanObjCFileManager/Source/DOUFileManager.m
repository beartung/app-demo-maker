//
//  DOUFileManager.m
//  DoubanGroup
//
//  Created by liu yan on 1/27/13.
//  Copyright (c) 2013 Douban. All rights reserved.
//

#import "DOUFileManager.h"
#include <sys/xattr.h>

NSString * const kDOUFMExpireDatesKey = @"DOUFileManager.expireDates";

static NSLock *gDOUFMSyncToUserDefaultsLock = nil;

@implementation DOUFileManager

#pragma mark - Shared Instance

+(DOUFileManager *)shareCacheFileInstance
{
  static DOUFileManager *cacheFileInstance = nil;
  static dispatch_once_t onceToken;
  dispatch_once(&onceToken, ^{
    NSArray *cachePaths = NSSearchPathForDirectoriesInDomains(NSCachesDirectory, NSUserDomainMask, YES);
    NSString *cachePath = [cachePaths objectAtIndex:0];
    cacheFileInstance = [[DOUFileManager alloc] initWithBaseFilePath:cachePath];
  });
  return cacheFileInstance;
}

+(DOUFileManager *)shareOfflineFileInstance
{
  static DOUFileManager *offlineInstance = nil;
  static dispatch_once_t onceToken;
  dispatch_once(&onceToken, ^{
    NSArray *libraryPaths = NSSearchPathForDirectoriesInDomains(NSLibraryDirectory, NSUserDomainMask, YES);
    NSString *offlinePath = [[libraryPaths objectAtIndex:0] stringByAppendingPathComponent:@"offline"];
    offlineInstance = [[DOUFileManager alloc] initWithBaseFilePath:offlinePath];
  });
  return offlineInstance;
 }

+(DOUFileManager *)shareTmpFileInstance
{
  static DOUFileManager *tmpFileInstance = nil;
  static dispatch_once_t onceToken;
  dispatch_once(&onceToken, ^{
    NSString *tmpPath = [NSHomeDirectory() stringByAppendingPathComponent:@"tmp"];
    tmpFileInstance = [[DOUFileManager alloc] initWithBaseFilePath:tmpPath];
  });
  return tmpFileInstance;
}

#pragma mark - init

-(id)initWithBaseFilePath:(NSString *)basePath
{
  self = [super init];
  if (self) {
    _baseFilePath = basePath;
    
    _expireDateDictionary = [[[NSUserDefaults standardUserDefaults] objectForKey:kDOUFMExpireDatesKey] objectForKey:self.baseFilePath];
    if (!_expireDateDictionary) {
      _expireDateDictionary = [NSMutableDictionary dictionary];
    }
  }
  return self;
}

#pragma mark - directory manager

-(NSString *)parseParentDirectoryAtPath:(NSString *)path
{
  NSString *parentDirPath = [self _absolutePathWithPath:path];
  NSMutableArray *pathArray = [NSMutableArray arrayWithArray:[parentDirPath componentsSeparatedByString:@"/"]];
  if ([pathArray count] > 1) {
    [pathArray removeLastObject];
    NSString *parentDirPath = [pathArray componentsJoinedByString:@"/"];
    return parentDirPath;
  } else {
    return nil;
  }
}

-(BOOL)createParentDirectoriesAtPath:(NSString *)path
{
  NSString *parentDirPath = [self parseParentDirectoryAtPath:path];
  BOOL success = [[NSFileManager defaultManager] createDirectoryAtPath:parentDirPath withIntermediateDirectories:YES attributes:nil error:NULL];
  
  NSURL *pathURL = [NSURL URLWithString:path];
  [self _addSkipBackupAttributeToItemAtURL:pathURL];
  return success;
}

-(BOOL)parentDirectoriesExistAtPath:(NSString *)path
{
  NSString *parentDirPath = [self parseParentDirectoryAtPath:path];
  return [[NSFileManager defaultManager] fileExistsAtPath:parentDirPath];
}

#pragma mark - Write File
-(BOOL)writeData:(NSData *)data atPath:(NSString *)path
{
  return [self writeData:data atPath:path expire:0];
}

-(BOOL)writeString:(NSString *)string atPath:(NSString *)path
{
  return [self writeString:string atPath:path expire:0];
}

-(BOOL)writeDictionary:(NSDictionary *)dictionary atPath:(NSString *)path
{
  return [self writeDictionary:dictionary atPath:path expire:0];
}

- (BOOL) writeArray:(NSArray *)array atPath:(NSString *)path
{
  return [self writeArray:array atPath:path expire:0];
}

-(BOOL)writeData:(NSData *)data atPath:(NSString *)path expire:(NSTimeInterval)expire
{
  if (![self parentDirectoriesExistAtPath:path]) {
    [self createParentDirectoriesAtPath:path];
  }
  
  NSString *finalPath = [self _absolutePathWithPath:path];
  
  [self setExpireTimeInterval:expire forFilePath:path];
  
  return [data writeToFile:finalPath atomically:YES];
}

-(BOOL)writeDictionary:(NSDictionary *)dictionary atPath:(NSString *)path expire:(NSTimeInterval)expire
{
  if (![self parentDirectoriesExistAtPath:path]) {
    [self createParentDirectoriesAtPath:path];
  }
  
  NSString *finalPath = [self _absolutePathWithPath:path];
  
  [self setExpireTimeInterval:expire forFilePath:path];
  
  return [dictionary writeToFile:finalPath atomically:YES];
}

-(BOOL)writeString:(NSString *)string atPath:(NSString *)path expire:(NSTimeInterval)expire {
  if (![self parentDirectoriesExistAtPath:path]) {
    [self createParentDirectoriesAtPath:path];
  }
  
  NSString *finalPath = [self _absolutePathWithPath:path];
  
  [self setExpireTimeInterval:expire forFilePath:path];
  
  return [string writeToFile:finalPath atomically:YES encoding:NSUTF8StringEncoding error:NULL];
}

- (BOOL) writeArray:(NSArray *)array atPath:(NSString *)path expire:(NSTimeInterval)expire
{
  if (![self parentDirectoriesExistAtPath:path]) {
    [self createParentDirectoriesAtPath:path];
  }
  
  NSString *finalPath = [self _absolutePathWithPath:path];
  
  [self setExpireTimeInterval:expire forFilePath:path];
  
  return [array writeToFile:finalPath atomically:YES];
}

#pragma mark - Delete
-(BOOL)deleteFileAtPath:(NSString *)path
{
  NSString *finalPath = [self _absolutePathWithPath:path];
  
  [_expireDateDictionary removeObjectForKey:path];
  [self _syncExpiredTimeToUserDefaults];
  
  return [[NSFileManager defaultManager] removeItemAtPath:finalPath error:NULL];
}

- (NSArray *)fileNamesInParentDirectory:(NSString *)path
{
  NSString *directoryPath = [self _absolutePathWithPath:path];
  NSString* filePath;
  NSDirectoryEnumerator* enumerator = [[NSFileManager defaultManager] enumeratorAtPath:directoryPath];
  NSMutableArray *fileNames = [NSMutableArray array];
  while (filePath = [enumerator nextObject])
  {
    BOOL isDirectory = NO;
    if ([[NSFileManager defaultManager] fileExistsAtPath: [NSString stringWithFormat:@"%@/%@",directoryPath,filePath]
                                             isDirectory: &isDirectory]) {
      if (!isDirectory)
      {
        [fileNames addObject:[filePath lastPathComponent]];
      }
    }
  }
  return fileNames;
}

#pragma mark - Read Files
- (NSString *) readStringAtPath:(NSString *)path
{
  NSString *finalPath = [self _absolutePathWithPath:path];
  if (!finalPath ||
      ![self fileVaildAtFilePath:path]) {
    return nil;
  }
  return [NSString stringWithContentsOfFile:finalPath encoding:NSUTF8StringEncoding error:NULL];
}

- (NSDictionary *) readDictionaryAtPath:(NSString *)path
{
  NSString *finalPath = [self _absolutePathWithPath:path];
  if (!finalPath ||
      ![self fileVaildAtFilePath:path]) {
    return nil;
  }
  return [NSDictionary dictionaryWithContentsOfFile:finalPath];
}

- (NSData *) readDataAtPath:(NSString *)path
{
  NSString *finalPath = [self _absolutePathWithPath:path];
  if (!finalPath ||
      ![self fileVaildAtFilePath:path]) {
    return nil;
  }
  return [NSData dataWithContentsOfFile:finalPath];
}

- (NSArray *)readArrayAtPath:(NSString *)path
{
  NSString *finalPath = [self _absolutePathWithPath:path];
  if (!finalPath ||
      ![self fileVaildAtFilePath:path]) {
    return nil;
  }
  return [NSArray arrayWithContentsOfFile:finalPath];
}

#pragma mark - expire
- (void) setExpireTimeInterval:(NSTimeInterval)expireTimeInterval forFilePath:(NSString *)filePath
{
  
  NSDate *expireDate = (expireTimeInterval > 0) ? [NSDate dateWithTimeIntervalSinceNow:expireTimeInterval] : [NSDate distantFuture];
  [_expireDateDictionary setObject:expireDate forKey:filePath];
  [self _syncExpiredTimeToUserDefaults];
}

- (BOOL) cleanExpireFile
{
  NSArray *allFilePathArray = [NSArray arrayWithArray:_expireDateDictionary.allKeys];
  for (NSString *fileKeyPath in allFilePathArray) {
    if ([self fileVaildAtFilePath:fileKeyPath]) {
      if (![self deleteFileAtPath:fileKeyPath]) {
        return NO;
      }
    }
  }
  return YES;
}

#pragma mark - File Vaild
- (BOOL) fileExpiredAtFilePath:(NSString *)filePath
{
  NSDate *expiredDate = [_expireDateDictionary objectForKey:filePath];
  if (!expiredDate ||
      [expiredDate timeIntervalSinceNow] >= 0) {
    return NO;
  } else {
    return YES;
  }
}

- (BOOL) fileExistsAtFilePath:(NSString *)filePath
{
  NSString *finalPath = [self _absolutePathWithPath:filePath];
  return [[NSFileManager defaultManager] fileExistsAtPath:finalPath];
}

- (BOOL) fileVaildAtFilePath:(NSString *)filePath
{
  if ([self fileExistsAtFilePath:filePath] &&
      ![self fileExpiredAtFilePath:filePath]) {
    return YES;
  }
  return NO;
}

#pragma mark - util
- (NSString *) _absolutePathWithPath:(NSString *)path
{
  NSString *finalPath = [self.baseFilePath stringByAppendingPathComponent:path];
  return finalPath;
}

- (BOOL)_addSkipBackupAttributeToItemAtURL:(NSURL *)URL {
  const char* filePath = [[URL path] fileSystemRepresentation];
  
  const char* attrName = "com.apple.MobileBackup";
  u_int8_t attrValue = 1;
  
  int result = setxattr(filePath, attrName, &attrValue, sizeof(attrValue), 0, 0);
  return result == 0;
}

- (void)_syncExpiredTimeToUserDefaults
{
  static dispatch_once_t onceToken;
  dispatch_once(&onceToken, ^{
    gDOUFMSyncToUserDefaultsLock = [[NSLock alloc] init];
  });
  
  [gDOUFMSyncToUserDefaultsLock lock];
  
  NSDictionary *dictionary = [[NSUserDefaults standardUserDefaults] objectForKey:kDOUFMExpireDatesKey];
  if (!dictionary) {
    dictionary = [NSMutableDictionary dictionary];
  }
  NSMutableDictionary *mutableDict = [NSMutableDictionary dictionaryWithDictionary:dictionary];
  [mutableDict setObject:_expireDateDictionary forKey:self.baseFilePath];
  [[NSUserDefaults standardUserDefaults] setObject:mutableDict forKey:kDOUFMExpireDatesKey];
  [[NSUserDefaults standardUserDefaults] synchronize];
  [gDOUFMSyncToUserDefaultsLock unlock];
}

@end
