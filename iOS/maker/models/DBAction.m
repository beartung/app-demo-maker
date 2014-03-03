//
//  DBAction.m
//  maker
//
//  Created by Bear on 2/22/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import "DBAction.h"

@implementation DBAction

-(id) initWithDict:(NSDictionary *)dict
{
    self = [super init];
    self.type = [dict valueForKey:@"type"];
    self.fromPageId = [dict valueForKey:@"page_id"];
    self.toPageId = [dict valueForKey:@"to_page_id"];
    self.dismiss = (int)[dict valueForKey:@"dismiss"] == 1;
    
    self.rect = CGRectMake([[dict valueForKey:@"x"] intValue]/2,
                           [[dict valueForKey:@"y"] intValue]/2,
                           [[dict valueForKey:@"width"] intValue]/2,
                           [[dict valueForKey:@"height"] intValue]/2);
    
    return self;
}

@end
