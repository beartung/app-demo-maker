//
//  DBEnv.h
//  maker
//
//  Created by Bear on 2/22/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "DBPage.h"

static NSString * const ACTION_TYPE_TOUCH       = @"T";
static NSString * const ACTION_TYPE_SLIDE       = @"LRUD";
static NSString * const ACTION_TYPE_SLIDE_LEFT  = @"L";
static NSString * const ACTION_TYPE_SLIDE_RIGHT = @"R";
static NSString * const ACTION_TYPE_SLIDE_UP    = @"U";
static NSString * const ACTION_TYPE_SLIDE_DOWN  = @"D";
static NSString * const ACTION_TYPE_BACK        = @"B";
static NSString * const ACTION_TYPE_INPUT       = @"I";
static NSString * const ACTION_TYPE_GALLERY     = @"G";
static NSString * const ACTION_TYPE_CAMERA      = @"C";
static NSString * const ACTION_TYPE_SHARE       = @"S";


static NSString * const PAGE_TYPE_NORMAL        = @"N";
static NSString * const PAGE_TYPE_LIST          = @"L";
static NSString * const PAGE_TYPE_PAGER         = @"P";
static NSString * const PAGE_TYPE_ITEM          = @"I";
static NSString * const PAGE_TYPE_DIALOG        = @"D";

@interface DBEnv : NSObject

@property (nonatomic, strong) NSString * id;
@property (nonatomic, strong) NSString * name;
@property (nonatomic, strong) NSString * icon;
@property (nonatomic, strong) NSString * api;
@property (nonatomic, strong) NSArray * pageIds;
@property (nonatomic, strong) NSDictionary * pages;

-(id) initWithDict:(NSDictionary *)dict;
-(DBPage *) getPage:(NSString *)id;

@end
