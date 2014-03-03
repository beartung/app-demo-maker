//
//  DBAction.h
//  maker
//
//  Created by Bear on 2/22/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface DBAction : NSObject

@property (nonatomic, strong) NSString * type;
@property (nonatomic, strong) NSString * fromPageId;
@property (nonatomic, strong) NSString * toPageId;
@property (nonatomic, assign) BOOL dismiss;
@property (nonatomic, assign) CGRect rect;


-(id) initWithDict:(NSDictionary *)dict;


@end
