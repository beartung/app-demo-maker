//
//  DBPage.h
//  maker
//
//  Created by Bear on 2/21/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "DBAction.h"

@interface DBPage : NSObject

@property (nonatomic, strong) NSString * id;
@property (nonatomic, strong) NSString * name;
@property (nonatomic, strong) NSString * parent;
@property (nonatomic, strong) NSString * type;
@property (nonatomic, strong) NSString * photo;
@property (nonatomic, strong) NSMutableArray * subPageIds;
@property (nonatomic, strong) NSMutableArray * actions;
@property (nonatomic, assign) CGRect rect;

-(id) initWithDict:(NSDictionary *)dict;

@end
