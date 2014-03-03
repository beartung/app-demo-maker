//
//  DBEnv.m
//  maker
//
//  Created by Bear on 2/22/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import "DBEnv.h"

@implementation DBEnv

-(id) initWithDict:(NSDictionary *)dict
{
    self = [super init];
    self.id = [dict valueForKey:@"id"];
    self.name = [dict valueForKey:@"name"];
    self.icon = [dict valueForKey:@"icon"];
    self.api = [dict valueForKey:@"api"];
    self.pageIds = [dict valueForKey:@"page_ids"];
    self.pages = [dict valueForKey:@"pages"];
    
    return self;
}

-(DBPage *) getPage:(NSString *)id
{
    return [[DBPage alloc] initWithDict:[self.pages valueForKey:id]];
}


@end
