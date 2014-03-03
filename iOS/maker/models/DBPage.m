//
//  DBPage.m
//  maker
//
//  Created by Bear on 2/21/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import "DBPage.h"

@implementation DBPage

-(id) initWithDict:(NSDictionary *)dict
{
    self = [super init];
    self.id = [dict valueForKey:@"id"];
    self.name = [dict valueForKey:@"name"];
    self.parent = [dict valueForKey:@"parent_id"];
    self.type = [dict valueForKey:@"type"];
    self.photo = [dict valueForKey:@"photo"];
    
    self.rect = CGRectMake([[dict valueForKey:@"x"] intValue]/2,
                           [[dict valueForKey:@"y"] intValue]/2,
                           [[dict valueForKey:@"width"] intValue]/2,
                           [[dict valueForKey:@"height"] intValue]/2);
    
    NSLog(@"page rect: %f, %f, %f, %f",
          self.rect.origin.x, self.rect.origin.y, self.rect.size.width, self.rect.size.height);
    
    NSArray * as = [dict valueForKey:@"actions"];
    self.actions = [[NSMutableArray alloc] init];
    for (int i = 0; i < as.count; i++){
        [self.actions addObject:[[DBAction alloc] initWithDict:as[i]]];
    }
    
    NSArray * sps = [dict valueForKey:@"sub_page_ids"];
    self.subPageIds = [[NSMutableArray alloc] init];
    for (int i = 0; i < sps.count; i++){
        [self.subPageIds addObject:sps[i]];
    }
    return self;
}

@end
